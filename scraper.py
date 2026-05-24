import os
import requests

# We are hitting their internal data system directly for this product ID
URL = "https://shop.amul.com/api/v1/en/products/amul-high-protein-rose-lassi-200-ml-or-pack-of-30"
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print("Querying Amul's backend stock database...")
    response = requests.get(URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Error accessing database: Status code {response.status_code}")
        return

    # Amul sends clean data back. Let's look inside it.
    data = response.json()
    
    # Extract the product status directly from their system
    try:
        product_info = data.get("data", {}).get("product", {})
        title = product_info.get("title", "Product")
        is_sold_out = product_info.get("isSoldOut", False)
        
        print(f"Successfully checked data for: {title}")
        
        if is_sold_out:
            print("System Confirmation: Item status is officially 'SOLD OUT'. Standing down.")
        else:
            print("🚨 ACTUAL STOCK DETECTED! Firing true alert to Discord! 🚨")
            send_discord_alert(title)
            
    except Exception as e:
        print(f"Could not parse the website data layout. Error details: {e}")

def send_discord_alert(item_title):
    if not DISCORD_WEBHOOK:
        print("Error: Webhook link missing in settings.")
        return
    
    public_url = "https://shop.amul.com/en/product/amul-high-protein-rose-lassi-200-ml-or-pack-of-30"
    payload = {
        "content": f"🚨 **AMUL RESTOCK DETECTED!** 🚨\n📦 **Item:** {item_title}\n🛒 **Buy now:** {public_url}"
    }
    requests.post(DISCORD_WEBHOOK, json=payload)
    print("True alert sent to Discord successfully.")

if __name__ == "__main__":
    check_stock()
