import os
import json

print("=== DARK FACTORY CREDENTIALS DIAGNOSTIC ===")
print()

# A. Verificar ambiente
print("A. ENVIRONMENT VARIABLES:")
print(f"   GEMINI_API_KEY exists: {'YES' if os.getenv('GEMINI_API_KEY') else 'NO'}")
print(f"   YOUTUBE_CREDENTIALS exists: {'YES' if os.getenv('YOUTUBE_CREDENTIALS') else 'NO'}")
print()

# B. Testar manualmente (substitua SEU_JSON_AQUI)
print("B. MANUAL TEST (substitua o JSON abaixo):")
test_json = '''SEU_JSON_AQUI'''

if test_json != 'SEU_JSON_AQUI':
    try:
        data = json.loads(test_json)
        print("   ✅ JSON is valid")
        print(f"   Structure: {list(data.keys())}")
        
        if 'installed' in data:
            installed = data['installed']
            print(f"   Installed keys: {list(installed.keys())}")
            print(f"   Client ID: {installed.get('client_id', 'MISSING')[:30]}...")
        else:
            print("   ⚠️  'installed' key not found")
            
    except json.JSONDecodeError as e:
        print(f"   ❌ JSON decode error: {e}")
    except Exception as e:
        print(f"   ❌ Error: {type(e).__name__}: {e}")
else:
    print("   ⚠️  Replace 'SEU_JSON_AQUI' with your actual JSON")
print()

# C. Problemas comuns
print("C. COMMON ISSUES:")
print("   1. JSON incomplete (copied partially)")
print("   2. Extra characters in JSON")
print("   3. Line breaks in JSON")
print("   4. Missing 'installed' key")
print()

print("=== NEXT STEPS ===")
print("1. Copy your ENTIRE JSON from Google Cloud")
print("2. Replace 'SEU_JSON_AQUI' above")
print("3. Run this script again")
