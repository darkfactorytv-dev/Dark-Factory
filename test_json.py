import json
import sys

print("Testing YouTube credentials...")

try:
    # Read the JSON file
    with open("creds.json", "r") as f:
        content = f.read()
    
    print(f"File size: {len(content)} characters")
    
    # Try to parse JSON
    data = json.loads(content)
    print("SUCCESS: JSON is valid")
    
    # Check structure
    if "installed" in data:
        print(f"Found 'installed' section")
        client_id = data["installed"].get("client_id", "")
        if client_id:
            print(f"Client ID: {client_id[:30]}...")
        else:
            print("WARNING: client_id not found")
    else:
        print("WARNING: 'installed' key not found")
        
    print("All checks passed!")
    
except FileNotFoundError:
    print("ERROR: creds.json file not found")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"ERROR: Invalid JSON - {e}")
    print(f"First 100 chars: {content[:100]}...")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    sys.exit(1)
