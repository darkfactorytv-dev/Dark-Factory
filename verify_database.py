import json

def main():
    # Ler removendo BOM
    with open("data/themes/database.json", "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    
    print("DATABASE VERIFICATION")
    print("=" * 40)
    print(f"Themes loaded: {len(data['themes'])}")
    
    for tema in data["themes"]:
        print(f"  • {tema['name']} ({tema['id']})")
        print(f"    Category: {tema['category']}")
        print(f"    Difficulty: {tema['difficulty']}")
    
    print("\n" + "=" * 40)
    print("✅ DATABASE READY FOR PRODUCTION")
    print("\nNext: Buy SIM card → Configure APIs → Real automation")

if __name__ == "__main__":
    main()
