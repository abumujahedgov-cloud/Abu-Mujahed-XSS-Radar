# 📡 ABU MUJAHED XSS RADAR v2.0
**Advanced Automated XSS Vulnerability Scanner & Deep Crawler**

---

## 📝 Description
**Abu Mujahed XSS Radar** is a professional security tool designed for bug hunters and penetration testers. It performs deep crawling into target domains, discovering hidden parameters, frames, and links to inject advanced XSS payloads.

## 🚀 Features
* **Deep Crawling:** Scans HTML, Frames, and IFrames for hidden links.
* **Smart Injection:** Automatically detects URL parameters and injects custom payloads.
* **Visual Evidence:** Automatically captures screenshots when a vulnerability is confirmed.
* **Headless/Headed Mode:** Watch the "Radar" in action or run it silently in the background.
* **Logging:** Saves all critical hits in a structured text file for reporting.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Abu-Mujahed-XSS-Radar.git](https://github.com/YOUR_USERNAME/Abu-Mujahed-XSS-Radar.git)
   cd Abu-Mujahed-XSS-Radar
   Install requirements:
You need to have Python installed. Then install the dependencies:

Bash
pip install playwright
playwright install chromium
💻 Usage
Run the tool and enter your target URL:

Bash
python3 deep_hunter.py
📂 Output
abu_mujahed_evidence/: Folder containing screenshots of confirmed hits.

ABU_MUJAHED_HITS.txt: A text file containing all the URLs and payloads that worked.

⚖️ Disclaimer
This tool is for educational purposes and ethical hacking only. Abu Mujahed is not responsible for any misuse or damage caused by this tool. Only use it on targets you have explicit permission to test.
