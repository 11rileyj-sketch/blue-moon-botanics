import config
import requests

# This is a 'Dummy' payload to trick Make.com into seeing the data structure
payload = {
    "common_name": "Queen Anne Fittonia",
    "scientific_name": "Fittonia albivenis",
    "care_summary": "Tampa-ready: Loves high humidity and indirect light. Keep soil moist!",
    "water": "💧 3x weekly",
    "sun": "☀️ Low to Medium",
    "cycle": "Perennial",
    "flowering": True,  # This is the 'Pill' we need to map!
    "photo_url": "https://trefle.io/api/v1/plants/placeholder.jpg",
    "raw_json": "{}"
}

print("Sending MOCK data to the docking bay...")
r = requests.post(config.MAKE_WEBHOOK_URL, json=payload)

if r.status_code == 200:
    print("SUCCESS: Mock data delivered! Go check Make.com.")
else:
    print(f"Failed: {r.status_code}")