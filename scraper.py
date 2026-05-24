import os
import requests
from bs4 import BeautifulSoup

URL = "https://shop.amul.com/en/product/amul-high-protein-rose-lassi-200-ml-or-pack-of-30" 
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print("Connecting to Amul...")
    response = requests.get(URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Error accessing site: Status code {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text().lower()

    # Diagnostic check: Let's see if the page actually contains core text
    print(f"Webpage data fetched. Total character count: {len(page_text)}")

    # Look for common stock text indicators on Amul's interface
    if "sold out" in page_text or "out of stock" in page_text:
        print("Verification: Found stock restriction text. Item is still unavailable. Standing down.")
    else:
        print("🚀 Stock indicator missing or flipped! Sending Discord Notification...")
        send_discord_alert()

def send_discord_alert():
    if not DISCORD_WEBHOOK:
        print("Error: DISCORD_WEBHOOK environment variable is empty!")
        return
    payload = {
        "content": f"🚀 **Amul stock update!** The High-Protein Rose Lassi might be back! Check here: {URL}"
    }
    r = requests.post(DISCORD_WEBHOOK, json=payload)
    print(f"Discord response status: {r.status_code}")

if __name__ == "__main__":
    check_stock()
