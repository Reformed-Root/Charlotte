# 🕷️ Charlotte's Web

An open-source web crawler for ethical cyber threat intelligence, focused on exposing fentanyl-related activity across the internet.

---

## 🧠 Overview

**Charlotte's Web** is a lightweight Python crawler developed under **Operation ReaperNet**, a mission to gather open-source intelligence (OSINT) on fentanyl and synthetic opioid distribution. It scrapes public websites, scans for high-risk keywords, and logs findings for analysis.

This project supports ethical cyber investigations and provides a foundation for building automated recon tools in the fight against digital narcotics trafficking.

---

## 🔍 Features

- ✅ Crawl public-facing websites  
- ✅ Scan for fentanyl-related keywords  
- ✅ Extract 40-character context around each hit  
- ✅ Timestamp and save results to a CSV  
- ✅ Easily customizable: keywords, URLs, output formats  

---

## 🧪 Sample Use Case
Target: https://en.wikipedia.org/wiki/Fentanyl
Keyword Match: "Fentanyl is a powerful synthetic opioid used in medicine..."
Logged: [URL, Keyword, Context, Timestamp]



---

## 🛠️ Tech Stack

- Python 3.13  
- `requests` – page retrieval  
- `BeautifulSoup` – HTML parsing  
- `re` – regex keyword detection  
- `csv`, `datetime` – logging/reporting  

---

## ⚙️ Future Plans

- [ ] Darknet (.onion) crawling via Tor proxy  
- [ ] Honeypot integration  
- [ ] Multi-threaded crawling  
- [ ] Daily scan scheduler (cron/Task Scheduler)  
- [ ] Visualization dashboard with graphs and alerts  

---

## ⚖️ Legal & Ethical Notice

Charlotte's Web is strictly for **legal and ethical purposes**.  
It only accesses **publicly available content**.  
It does **not** interact with illegal services or hidden transactions.

> Always use this software responsibly and within the law.

---

## 🙏 Credit & Mission

**Built by Reformed-Root CyberSolutions** — cybersecurity student, reformed fighter, and defender of the people.

> "I built this tool to monitor the digital networks poisoning our streets.  
> This isn’t just code — it’s a response."

---

## 📦 Installation

Make sure Python 3 is installed. Then run:

```bash
pip install -r requirements.txt
```


