import os
import cloudscraper
import requests
from bs4 import BeautifulSoup

URL = "https://shop.amul.com/en/product/amul-high-protein-rose-lassi-200-ml-or-pack-of-30" 
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

def check_stock():
    print("Putting on our VIP disguise (Cloudscraper) to bypass Amul's bouncers...")
    
    # Create a scraper that perfectly mimics a real Chrome browser on Windows
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False
    })
    
    response = scraper.get(URL)
    
    if response.status_code != 200:
        print(f"Error accessing site: Status code {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text().lower()

    char_count = len(page_text)
    print(f"Webpage data fetched. Total character count: {char_count}")

    if char_count < 1000:
        print("Uh oh, character count is still suspiciously low. The bouncer caught us.")
        return

    # Check for the stock text
    if "sold out" in page_text or "out of stock" in page_text:
        print("Verification: Found stock restriction text. Item is still unavailable. Standing down.")
    else:
        print("🚀 TEXT LOADED AND ITEM IN STOCK! Sending Discord Notification...")
        send_discord_alert()

def send_discord_alert():
    if not DISCORD_WEBHOOK:
        print("Error: DISCORD_WEBHOOK environment variable is empty!")
        return
    payload = {
        "content": f"🚀 **Amul stock update!** The High-Protein Rose Lassi is back! Check here: {URL}"
    }
    requests.post(DISCORD_WEBHOOK, json=payload)
    print("Discord alert fired!")

if __name__ == "__main__":
    check_stock()
