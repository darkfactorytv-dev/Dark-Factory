import json
import os
from datetime import datetime

print("DARK FACTORY - FINAL SYSTEM CHECK")
print("=" * 50)

# 1. Check essential files
print("\n1. ESSENTIAL FILES:")
essential_files = [
    ("data/themes/database.json", "Themes Database"),
    ("src/utils/logger.py", "Logger System"),
    ("src/core/theme_manager.py", "Theme Manager"),
]

all_ok = True
for file_path, description in essential_files:
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"   ✓ {description}: {file_path} ({size} bytes)")
    else:
        print(f"   ✗ {description}: MISSING")
        all_ok = False

# 2. Check database
print("\n2. DATABASE CHECK:")
try:
    with open("data/themes/database.json", "r", encoding="utf-8-sig") as f:
        db = json.load(f)
    
    themes_count = len(db.get("themes", []))
    print(f"   ✓ Themes in database: {themes_count}")
    
    if themes_count > 0:
        sample_theme = db["themes"][0]
        print(f"   ✓ Sample theme: {sample_theme.get('name')} ({sample_theme.get('id')})")
    
except Exception as e:
    print(f"   ✗ Database error: {e}")
    all_ok = False

# 3. Project structure
print("\n3. PROJECT STRUCTURE:")
folders = ["src", "data", "logs", "productions"]
for folder in folders:
    if os.path.exists(folder):
        print(f"   ✓ {folder}/")
    else:
        print(f"   ✗ {folder}/ (missing)")

# 4. Summary
print("\n" + "=" * 50)
if all_ok:
    print("✅ SYSTEM READY FOR API INTEGRATION")
    print("\nNEXT STEPS (Tomorrow with SIM card):")
    print("  1. Buy prepaid SIM card (R$ 15-20)")
    print("  2. Add number to Google account")
    print("  3. Create YouTube Channel")
    print("  4. Verify channel (required for upload)")
    print("  5. Configure Google Cloud APIs")
    print("  6. Get OAuth 2.0 tokens")
else:
    print("⚠️  SYSTEM NEEDS ADJUSTMENTS")
    print("  Run: python verify_database.py")

print("\n" + "=" * 50)
print(f"Check completed: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
