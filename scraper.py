import os
import requests
from bs4 import BeautifulSoup

# The URL we actually want to check
AMUL_URL = "https://shop.amul.com/en/product/amul-high-protein-rose-lassi-200-ml-or-pack-of-30" 

# Our secret vault keys
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
SCRAPER_API_KEY = os.environ.get("SCRAPER_API_KEY")

def check_stock():
    print("Asking ScraperAPI to check Amul using a residential proxy...")
    
    # We send our target URL to ScraperAPI instead of going directly to Amul
    payload = {
        'api_key': SCRAPER_API_KEY,
        'url': AMUL_URL,
        'render': 'true' # Tells ScraperAPI to wait for the JavaScript text to load
    }
    
    response = requests.get('https://api.scraperapi.com/', params=payload)
    
    if response.status_code != 200:
        print(f"Proxy Error: Status code {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text().lower()

    char_count = len(page_text)
    print(f"Webpage data fetched via proxy. Total character count: {char_count}")

    if char_count < 1000:
        print("Bouncer still caught us, or page didn't render fully.")
        return

    if "sold out" in page_text or "out of stock" in page_text:
        print("Verification: Item is still Sold Out. Standing down.")
    else:
        print("🚀 TEXT LOADED AND ITEM IN STOCK! Firing Discord Alert! 🚨")
        send_discord_alert()

def send_discord_alert():
    if not DISCORD_WEBHOOK:
        print("Error: Webhook link missing.")
        return
    payload = {
        "content": f"🚀 **Amul stock update!** The High-Protein Rose Lassi is back! Check here: {AMUL_URL}"
    }
    requests.post(DISCORD_WEBHOOK, json=payload)
    print("Discord alert fired!")

if __name__ == "__main__":
    check_stock()
