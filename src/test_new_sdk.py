#!/usr/bin/env python3
"""Quick test of new google-genai SDK"""
import google.genai
from darker_factory import decode_credentials

print("🧪 Testing new google-genai SDK...")
print("=" * 40)

# Get credentials
api_key, _ = decode_credentials()
if not api_key:
    print("❌ No API key")
    exit(1)

print(f"API key: {api_key[:15]}...")

try:
    # NEW API
    client = google.genai.Client(api_key=api_key)
    print("✅ Client created successfully")
    
    # List models
    models = list(client.models.list())
    print(f"✅ Models available: {len(models)}")
    
    # Try a simple generation
    print("Testing generation...")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Say 'Dark Factory is working!'"
    )
    
    print(f"✅ Generation test: {response.text}")
    print("🎉 NEW SDK WORKING CORRECTLY!")
    
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
