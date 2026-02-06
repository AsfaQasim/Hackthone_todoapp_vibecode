"""Test if OpenAI API key is valid."""

import os
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv('OPENAI_API_KEY')

if not openai_key:
    print("❌ No OpenAI API key found in .env")
    exit(1)

print(f"OpenAI API Key found: {openai_key[:20]}...")

# Test the key
try:
    from openai import OpenAI
    client = OpenAI(api_key=openai_key)
    
    print("\nTesting API key with a simple request...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'test successful'"}],
        max_tokens=10
    )
    
    print(f"✅ API key is valid!")
    print(f"   Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ API key test failed: {e}")
    print(f"\nThis is likely why the chat endpoint is failing.")
