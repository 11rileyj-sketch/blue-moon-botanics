import requests

# HARDCODE the keys as raw strings just for this test
# Click "Show key" in your screenshot to copy the raw Blue Moon key
API_KEY = "AIzaSyDqKrMtlWnr9v3I4X7xfWbIU1jEkH2A1LQ"  
CX = "d68ee39b7d43b4b1f"        

url = "https://customsearch.googleapis.com/customsearch/v1"
params = {
    "key": API_KEY,
    "cx": CX,
    "q": "foxtail fern houseplant",
    "searchType": "image",
    "num": 1
}

response = requests.get(url, params=params)

if response.status_code == 200:
    print("✅ SUCCESS! The Cloud configuration is perfect.")
    print(response.json()['items'][0]['link'])
else:
    print(f"❌ FAILED: {response.status_code}")
    print(response.json())