import os
import sys
from google import genai

# Look one folder up for config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import config
    print("✅ Config found!")
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    print("🚀 Connection successful! Fetching available models...")
    
    # We'll just print the ID and the human-readable name for every model
    for model in client.models.list():
        print(f" - ID: {model.name} | Title: {model.display_name}")
        
except ImportError:
    print("❌ Error: Still can't find config.py.")
except Exception as e:
    print(f"❌ Connection Error: {e}")