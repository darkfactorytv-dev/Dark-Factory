#!/usr/bin/env python3
"""
Test YouTube OAuth credentials
"""
import json
import os
import sys

def main():
    print("🔍 Testing YouTube Credentials")
    print("=" * 50)
    
    # Read from environment variable
    creds_json = os.getenv("YOUTUBE_CREDENTIALS")
    if not creds_json:
        print("❌ ERROR: YOUTUBE_CREDENTIALS environment variable is empty")
        print("   Configure it in GitHub: Settings > Secrets > Actions")
        return 1
    
    print(f"✅ Raw data length: {len(creds_json)} characters")
    
    # Save to file for inspection
    with open("youtube_creds_debug.json", "w") as f:
        f.write(creds_json)
    print("📁 Saved to: youtube_creds_debug.json")
    
    # Try to parse JSON
    try:
        data = json.loads(creds_json)
        print("✅ JSON syntax is valid")
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"First 200 chars: {creds_json[:200]}...")
        return 1
    
    # Check structure
    if "installed" not in data:
        print("❌ ERROR: Missing 'installed' key in JSON")
        print(f"Available keys: {list(data.keys())}")
        return 1
    
    installed = data["installed"]
    print("✅ Found 'installed' section")
    
    # Check required fields
    required = ["client_id", "client_secret", "auth_uri", "token_uri"]
    missing = [field for field in required if field not in installed]
    
    if missing:
        print(f"❌ Missing required fields: {missing}")
        print(f"Available fields: {list(installed.keys())}")
        return 1
    
    print("✅ All required fields present")
    print(f"   Client ID: {installed['client_id'][:30]}...")
    print(f"   Auth URI: {installed['auth_uri']}")
    
    print("=" * 50)
    print("🎉 SUCCESS: YouTube credentials are valid!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
