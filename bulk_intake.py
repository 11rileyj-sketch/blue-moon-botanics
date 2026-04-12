import config
import requests
import json
import time
import os
from google import genai

# Setup the Gemini Client
client = genai.Client(api_key=config.GEMINI_API_KEY)

# --- THE LOG BOOK ---
LOG_FILE = "processed_plants.txt"

# --- THE LOADING DOCK (The Starting Five) ---
PLANT_LIST = [
    "Queen Anne Fittonia",
    "English Lavender",
    "Moon Valley Pilea",
    "Zebra Plant",
    "Lemon Lime Pothos"
]

def get_processed_plants():
    if not os.path.exists(LOG_FILE):
        return set()
    with open(LOG_FILE, "r") as f:
        return set(line.strip() for line in f)

def log_finished_plant(plant_name):
    with open(LOG_FILE, "a") as f:
        f.write(f"{plant_name}\n")

def get_trefle_image(scientific_name):
    search_url = f"https://trefle.io/api/v1/plants/search?token={config.TREFLE_TOKEN}&q={scientific_name}"
    try:
        r = requests.get(search_url).json()
        if r.get('data') and len(r['data']) > 0:
            url = r['data'][0].get('image_url')
            if url: return url
        return None
    except:
        return None

def process_plant(plant_name):
    print(f"\n🚀 Processing: {plant_name}...")
    
    prompt = f"""
    Create a botanical profile for '{plant_name}' for a grower in Tampa, FL. 
    Return strictly JSON:
    - common_name: Standard name
    - scientific_name: Latin name
    - tampa_care_summary: 2-3 sentences on FL indoor/outdoor care.
    - water: '💧 frequency'
    - sun: '☀️ requirement'
    - cycle: (Perennial, Annual, or Biennial)
    - flowering: True/False
    """

    try:
        # SWITCHED TO 1.5 FLASH based on your dashboard availability
        response = client.models.generate_content(model='gemini-1.5-flash', contents=prompt)
        raw_json_str = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(raw_json_str)

        photo = get_trefle_image(data['scientific_name'])

        payload = {
            "common_name": data['common_name'],
            "scientific_name": data['scientific_name'],
            "care_summary": data['tampa_care_summary'],
            "water": data['water'],
            "sun": data['sun'],
            "cycle": data['cycle'],
            "flowering": data['flowering'],
            "photo_url": photo,
            "raw_json": raw_json_str
        }

        requests.post(config.MAKE_WEBHOOK_URL, json=payload)
        log_finished_plant(plant_name)
        print(f"✅ SUCCESS: {plant_name} is in the gallery.")

    except Exception as e:
        print(f"❌ FAILED {plant_name}: {e}")

if __name__ == "__main__":
    processed = get_processed_plants()
    to_process = [p for p in PLANT_LIST if p not in processed]
    
    print(f"Checking memory... {len(processed)} plants already done.")
    print(f"Starting intake for {len(to_process)} new plants using 1.5 Flash...")

    for plant in to_process:
        process_plant(plant)
        print("Waiting 12s for a safe cooldown...")
        time.sleep(12) # Slightly longer sleep to be extra safe
        
    print("\nMission Complete. Check your Airtable!")