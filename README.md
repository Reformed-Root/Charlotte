🕷️ Charlotte
An open-source web crawler for open-source intelligence (OSINT) collection.

Overview:
Charlotte is a lightweight Python-based crawler designed for OSINT tasks. It retrieves public web pages, scans for custom keywords, and logs contextual hits for analysis.

The project is intended for security researchers, analysts, and developers who need a flexible foundation for building automated reconnaissance and data-gathering workflows.

Features:
✅ Crawl public-facing websites

✅ Scan for user-defined keywords

✅ Extract 40-character context around each match

✅ Timestamp and save results to CSV

✅ Multi-threaded crawling

✅ Easily customizable (keywords, URLs, output format)

Sample Use Case:
Example Target: https://en.wikipedia.org/wiki/Open-source_intelligence
Example Keyword Match: "Open-source intelligence (OSINT) is..."
Logged Output: [URL, Keyword, Context, Timestamp]

Tech Stack:
Python 3.13

requests – page retrieval

BeautifulSoup – HTML parsing

re – regular expression matching

csv, datetime – logging and reporting

Planned Improvements:
 Support for Tor proxy and .onion sites

 Daily scan scheduling (cron/Task Scheduler)

 Visualization dashboard with graphs and alerts

Legal & Ethical Notice:
Charlotte is intended for legal and ethical OSINT activities.
It only accesses publicly available content and does not interact with hidden services or private data.

Always ensure you have permission to crawl target sites and comply with their terms of service.

Credits:
Created by John Kearney — cybersecurity professional and aspiring full-stack developer.

I built Charlotte as a personal project to make OSINT tasks easier and more repeatable. It’s free to use and modify — feel free to improve it or adapt it for your own work! 
---

## 📦 Installation

Make sure Python 3 is installed. Then run:

```bash
pip install -r requirements.txt
```


