import google.generativeai as genai
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.api_keys import api_key_manager

key = api_key_manager.get_key()
if not key:
    print("No API key found in .env")
    sys.exit(1)

genai.configure(api_key=key)

print("Available models:")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
