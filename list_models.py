import config
from google import genai

client = genai.Client(api_key=config.GEMINI_API_KEY)

print("--- SCANNING FOR AVAILABLE ENGINES ---")
try:
    # This just asks for the name of every model your key can see
    for model in client.models.list():
        print(f"Engine ID: {model.name}")
except Exception as e:
    print(f"Failed to scan engines: {e}")