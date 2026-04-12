import sys
import os
import requests
import json

# --- 1. ENVIRONMENT SETUP ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try: 
    import config
except ImportError: 
    sys.exit("❌ Error: Missing config.py")

def scout_mouser(part_name):
    if not hasattr(config, 'MOUSER_API_KEY') or config.MOUSER_API_KEY == "PASTE_KEY_HERE":
        print("❌ Error: Mouser API Key is missing or not set in config.py")
        return

    print(f"🔍 Scouting Mouser for: '{part_name}'...")
    
    url = f"https://api.mouser.com/api/v2/search/partnumber?key={config.MOUSER_API_KEY}"
    payload = {
        "SearchByPartRequest": {
            "mouserPartNumber": part_name,
            "partSearchOptions": "string"
        }
    }

    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        data = response.json()
        
        parts = data.get('SearchResults', {}).get('Parts', [])
        
        if not parts:
            print(f"⚠️  No matches found for '{part_name}'.")
            return

        # Show the top result
        part = parts[0]
        print("\n--- 🐭 MOUSER DATA FOUND ---")
        print(f"Manufacturer: {part.get('Manufacturer')}")
        print(f"MPN:          {part.get('ManufacturerPartNumber')}")
        print(f"Description:  {part.get('Description')}")
        
        docs = part.get('Documents', [])
        pdf = next((d['DocPath'] for d in docs if '.pdf' in d.get('DocPath', '').lower()), "No PDF Found")
        print(f"Datasheet:    {pdf}")
        print("---------------------------\n")

    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: scout <part_name>")
    else:
        scout_mouser(" ".join(sys.argv[1:]))