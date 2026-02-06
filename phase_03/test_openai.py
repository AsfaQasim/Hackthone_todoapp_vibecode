"""Test OpenAI API key"""
import os
from dotenv import load_dotenv

# Load from backend/.env
load_dotenv("backend/.env")

api_key = os.getenv("OPENAI_API_KEY")

print(f"API Key found: {bool(api_key)}")
print(f"API Key length: {len(api_key) if api_key else 0}")
print(f"API Key starts with: {api_key[:20] if api_key else 'N/A'}...")

# Try to use it
try:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=10
    )
    
    print(f"\n✅ OpenAI API is working!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"\n❌ OpenAI API error: {e}")
