#!/usr/bin/env python3
"""
Dark Factory - System Check
Validates all dependencies and credentials
Uses NEW google-genai SDK
"""
import os
import json
import sys
import google.genai  # NEW SDK

def check_gemini():
    """Check Gemini API credentials with NEW SDK"""
    print("🔍 Checking Gemini API (new SDK)...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Fallback to embedded credentials
    if not api_key:
        try:
            from darker_factory import decode_credentials
            api_key, _ = decode_credentials()
        except:
            api_key = ""
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return False
    
    try:
        # NEW API: Create client
        client = google.genai.Client(api_key=api_key)
        
        # Test by listing models
        models = list(client.models.list())
        print(f"✅ Gemini API: OK ({len(models)} models available)")
        
        # Show available models
        print("   Available models:")
        for model in models[:3]:  # Show first 3
            print(f"     - {model.name}")
        if len(models) > 3:
            print(f"     ... and {len(models)-3} more")
            
        return True
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return False

def check_youtube():
    """Check YouTube credentials"""
    print("🔍 Checking YouTube credentials...")
    
    creds_json = os.getenv("YOUTUBE_CREDENTIALS")
    
    # Fallback to embedded credentials
    if not creds_json:
        try:
            from darker_factory import decode_credentials
            _, creds_json = decode_credentials()
        except:
            creds_json = ""
    
    if not creds_json:
        print("❌ YOUTUBE_CREDENTIALS not found")
        return False
    
    try:
        data = json.loads(creds_json)
        
        if "installed" not in data:
            print("❌ Missing 'installed' key in JSON")
            return False
        
        required = ["client_id", "client_secret", "auth_uri", "token_uri"]
        installed = data["installed"]
        missing = [field for field in required if field not in installed]
        
        if missing:
            print(f"❌ Missing required fields: {missing}")
            return False
        
        print(f"✅ YouTube credentials: OK")
        print(f"   Client ID: {installed['client_id'][:30]}...")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_python():
    """Check Python version and dependencies"""
    print("🔍 Checking Python environment...")
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check required packages
    required = ["google-genai", "google-auth-oauthlib", "google-api-python-client"]
    
    for package in required:
        try:
            if package == "google-genai":
                __import__("google.genai")
            elif package == "google-auth-oauthlib":
                __import__("google_auth_oauthlib")
            elif package == "google-api-python-client":
                __import__("googleapiclient")
            print(f"✅ {package}: OK")
        except ImportError:
            print(f"❌ {package}: Missing")
            return False
    
    return True

def main():
    print("🏭 DARK FACTORY - SYSTEM CHECK (NEW SDK)")
    print("=" * 50)
    
    checks = [
        ("Python", check_python()),
        ("Gemini API", check_gemini()),
        ("YouTube API", check_youtube())
    ]
    
    print("\n" + "=" * 50)
    print("📊 RESULTS:")
    
    all_passed = True
    for name, passed in checks:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 SYSTEM READY FOR PRODUCTION!")
        return 0
    else:
        print("⚠️  SYSTEM CHECK FAILED - Fix issues above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
