import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime

# ===Operation ReaperNet Config== #
target_urls = [
    "https://target_url",
    "https://en.wikipedia.org/wiki/fentanyl"
]

keywords = [
    "fentanyl", "xylazine", "precursor", "acetylfentanyl",
    "carfentanil", "analogue", "hydrochloride", "RC chemical",
    "synth", "bulk powder", "darknet pills", "blues", "m-30s", 
    "m30s", "fet", "fent", "fetty" 
]

output_file = "charlotte's_web.csv"

def charlotte(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text().lower()
        hits = []

        for keyword in keywords:
            for match in re.finditer(rf"(.{{0,40}}{re.escape(keyword)}.{{0,40}})", text):
                context = match.group(0).strip()
                hits.append((url, keyword, context, datetime.utcnow().isoformat()))
        return hits
    except Exception as e:
        print(f"[ERROR] Could Not Scan {"url"}: {e}")
        return[]
    
def charlottes_web(results):
    with open(output_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for entry in results:
            writer.writerow(entry)

def main():
    print("**==Operation ReaperNet Launching==**")
    for url in target_urls:
        print(f"[*] Scanning: {url}")
        results = charlotte(url)
        if results:
            print(f"[+] {len(results)} hits found.")
            charlottes_web(results)
        else:
            print("[-] No matches.")
    print("**==Mission Complete==**")

if __name__=="__main__":
    # Write headers if file doesn't exist
    try:
        with open(output_file, 'x', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(["URL", "Keyword", "Context", "Timestamp"])
    except FileExistsError:
        pass  # Don't overwrite existing file
    main()