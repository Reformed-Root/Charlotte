import requests  # For sending HTTP requests to target URLs
from bs4 import BeautifulSoup  # For parsing HTML and extracting text
import re  # For searching keyword matches using regular expressions
import csv  # For writing results to a CSV file
from datetime import datetime, timezone
  # For adding timestamps to results
from urllib.parse import urljoin, urlparse
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
import time, random


# === Charlotte's Config === #

# === Clear old CSV results before new scan === #
output_file = "charlotte's_web.csv"
with open(output_file, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["URL", "Keyword", "Context", "Timestamp"])


# List of keywords associated with fentanyl and synthetic opioids
keywords = [
    "fentanyl","fetynal","xylazine", "precursor", "acetylfentanyl",
    "carfentanil", "analogue", "hydrochloride", "RC chemical",
    "synth", "bulk powder", "darknet pills", "blues", "m-30s",
    "m30s", "fet", "fent", "fetty",
    "fentanilo", "xilazina", "precursor", "acetilfentanilo",
    "carfentanilo", "análogo", "hidrocloruro", "químico rc",
    "sintético", "polvo a granel", "pastillas del mercado negro",
    "azules", "fenta", "芬太尼",
    "赛拉嗪", "前体", "乙酰芬太尼", "卡芬太尼",
    "类似物", "盐酸盐", "研究化学品", "合成毒品",
    "散装粉末", "暗网药丸", "蓝色药丸", "M-30", "M30",
    "芬太", "芬太尼毒品"
]


# Output CSV file to store results
output_file = "charlotte's_web.csv"

def get_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
    ]

    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

# === Main scanning function === #
def charlotte(url):
    try:
        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'no-cache',

}

        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, "html.parser")  # Parse the HTML content
        text = soup.get_text().lower()  # Extract all text and convert to lowercase for keyword matching
        print(f"[DEBUG] Scanning {url} — first 500 chars:")
        print(text[:500])

        hits = []

        # Search for each keyword in the text using regular expressions
        for keyword in keywords:
            for match in re.finditer(rf"(.{{0,40}}{re.escape(keyword)}.{{0,40}})", text):
                context = match.group(0).strip()  # Capture 40 characters before and after the keyword
                hits.append((url, keyword, context, datetime.now(timezone.utc).isoformat()
))  # Append result with timestamp
        return hits
    except Exception as e:
        print(f"[ERROR] Could Not Scan {url}: {e}")  # Handle network/parse errors gracefully
        return []

def random_delay():
    time.sleep(random.uniform(2, 6)) # Delays 2-6 seconds

def crawl_domain(base_url):
    global all_hits
    visited = set()
    #queue = deque([base_url])
    all_hits = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:    
        response = requests.get(base_url, headers=headers, timeout=10)
        response.encoding = response.apparent_encoding

        final_url = response.url  # Follow redirect
        base_domain = urlparse(final_url).netloc
        queue = deque([final_url])  # Start from the actual page
    except Exception as e:
        print(f"[ERROR] Could not reach domain: {e}")
        return []

    # Main crawl loop
    while queue:
        current_batch = []

        # Batch up to 10 new URLs
        while queue and len(current_batch) < 10:
            url = queue.popleft()
            if url not in visited:
                visited.add(url)
                current_batch.append(url)

        # Use ThreadPoolExecutor to scan current batch
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_to_url = {executor.submit(charlotte, url): url for url in current_batch}

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    hits = future.result()
                    all_hits.extend(hits)
                except Exception as e:
                    print(f"[ERROR] Failed to scan {url}: {e}")

        # Now that pages are scanned, extract links (single-threaded)
        for url in current_batch:
            try:
                res = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(res.text, "html.parser")

                # Find all internal links
                for tag in soup.find_all("a", href=True):
                    href = tag["href"]
                    full_url = urljoin(url, href)
                    target_domain = urlparse(full_url).netloc

                    if target_domain == base_domain and full_url not in visited and full_url not in queue:
                        queue.append(full_url)

            except Exception as e:
                print(f"[ERROR] Could not crawl {url}: {e}")
    return all_hits


# === Save scan results to CSV === #
def charlottes_web(results):
    with open(output_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for entry in results:
            writer.writerow(entry)  # Write each hit as a row in the CSV

# === Entry point for the program === #
def main():
    print("**== Operation ReaperNet: Domain Recon Mode ==**")
    domain = input("Enter a domain to crawl (e.g. https://example.com): ").strip()
   
    
    try:
        results = crawl_domain(domain)
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user. Saving progress...")

        # Save anything collected so far
        if 'all_hits' in globals() and all_hits:
            charlottes_web(all_hits)
            print(f"[+] {len(all_hits)} partial results saved.")
        else:
            print("[-] No results to save.")
        return

    if results:
        print(f"[+] {len(results)} total matches found during domain crawl.")
        charlottes_web(results)
    else:
        print("[-] No matches found in domain.")

    print("**== Mission Complete ==**")


# === Run only if script is executed directly === #
if __name__ == "__main__":
    # Check if output file exists, create it with headers if not
    try:
        with open(output_file, 'x', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(["URL", "Keyword", "Context", "Timestamp"])
    except FileExistsError:
        pass  # Do nothing if file already exists
    main()  # Launch the scanner
