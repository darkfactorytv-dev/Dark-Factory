import json

def main():
    with open("data/themes/database.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"📊 Temas carregados: {len(data['themes'])}")
    
    for tema in data["themes"]:
        print(f"   • {tema['name']} ({tema['id']})")

if __name__ == "__main__":
    main()
