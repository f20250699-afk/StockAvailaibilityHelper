import os
import requests
from bs4 import BeautifulSoup

# 1. Paste your exact Amul product link inside the quotes below!
URL = "https://shop.amul.com/en/product/amul-high-protein-rose-lassi-200-ml-or-pack-of-30" 
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

def check_stock():
    # Fake browser identity so Amul's servers treat us like a regular human visitor
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    print(f"Checking Amul website for product...")
    response = requests.get(URL, headers=headers)
    
    # Check if the page loaded successfully
    if response.status_code != 200:
        print(f"Error: Couldn't access the site. Code: {response.status_code}")
        return

    # Convert the Amul webpage layout into lowercase text
    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text().lower()

    # 2. Amul Logic: Look for the phrase "sold out"
    if "sold out" in page_text:
        print("Item is still Sold Out. Standing down.")
    else:
        print("🚨 AMUL ITEM IS BACK IN STOCK! Firing Discord Alert! 🚨")
        send_discord_alert()

def send_discord_alert():
    payload = {
        "content": f"🚀 **Amul stock update!** The item is back! Buy it now: {URL}"
    }
    # Send the alert message directly to your Discord channel
    requests.post(DISCORD_WEBHOOK, json=payload)

if __name__ == "__main__":
    check_stock()
