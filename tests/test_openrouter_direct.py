#!/usr/bin/env python3
"""
Direct OpenRouter API Test
"""

import os
import requests
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_openrouter_api():
    """Test OpenRouter API directly."""
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    print(f"API Key present: {bool(api_key)}")
    print(f"API Key length: {len(api_key) if api_key else 0}")
    
    if not api_key:
        print("❌ No OpenRouter API key found")
        return
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://sage-assistant.local",
        "X-Title": "SAGE AI Assistant"
    }
    
    # Simple test payload
    payload = {
        "model": "qwen/qwen-2.5-coder-32b-instruct",  # Try a different model first
        "messages": [
            {"role": "user", "content": "Write a simple Python function that prints 'Hello World'"}
        ],
        "max_tokens": 100,
        "temperature": 0.1
    }
    
    try:
        print("🔍 Testing OpenRouter API...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API call successful!")
            print(f"Model: {result.get('model', 'Unknown')}")
            content = result['choices'][0]['message']['content']
            print(f"Response: {content[:100]}...")
        else:
            print("❌ API call failed")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_openrouter_api()