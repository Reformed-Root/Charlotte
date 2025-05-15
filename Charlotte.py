import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime

# ===Operation ReaperNet Config== #
target_urls = [
    "https://target_url",  # Replace with actual URL targets
    "https://en.wikipedia.org/wiki/fentanyl"
]

# List of keywords associated with fentanyl and synthetic opioids
keywords = [
    "fentanyl", "xylazine", "precursor", "acetylfentanyl",
    "carfentanil", "analogue", "hydrochloride", "RC chemical",
    "synth", "bulk powder", "darknet pills", "blues", "m-30s", 
    "m30s", "fet", "fent", "fetty"
]

# Output CSV file to store results
output_file = "charlotte's_web.csv"

# === Main scanning function === #
def charlotte(url):
    try:
        response = requests.get(url, timeout=10)  # Make a GET request to the URL
        soup = BeautifulSoup(response.text, "html.parser")  # Parse the HTML content
        text = soup.get_text().lower()  # Extract all text and convert to lowercase for keyword matching
        hits = []

        # Search for each keyword in the text using regular expressions
        for keyword in keywords:
            for match in re.finditer(rf"(.{{0,40}}{re.escape(keyword)}.{{0,40}})", text):
                context = match.group(0).strip()  # Capture 40 characters before and after the keyword
                hits.append((url, keyword, context, datetime.utcnow().isoformat()))  # Append result with timestamp
        return hits
    except Exception as e:
        print(f"[ERROR] Could Not Scan {url}: {e}")  # Handle network/parse errors gracefully
        return []

# === Save scan results to CSV === #
def charlottes_web(results):
    with open(output_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for entry in results:
            writer.writerow(entry)  # Write each hit as a row in the CSV

# === Entry point for the program === #
def main():
    print("**==Operation ReaperNet Launching==**")
    for url in target_urls:
        print(f"[*] Scanning: {url}")
        results = charlotte(url)
        if results:
            print(f"[+] {len(results)} hits found.")
            charlottes_web(results)  # Log hits to file
        else:
            print("[-] No matches.")
    print("**==Mission Complete==**")

# === Run only if script is executed directly === #
if __name__ == "__main__":
    # Check if output file exists, create it with headers if not
    try:
        with open(output_file, 'x', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(["URL", "Keyword", "Context", "Timestamp"])
    except FileExistsError:
        pass  # Don't overwrite existing file
    main()