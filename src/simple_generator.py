#!/usr/bin/env python3
"""
Dark Factory - Simple Content Generator (Fallback)
"""
import random
from datetime import datetime

def generate_simple_content():
    """Generate simple content without Gemini API"""
    print("🎬 DARK FACTORY - SIMPLE GENERATOR")
    print("=" * 50)
    
    # Templates simples
    templates = [
        {
            "title": "The Future of Automated Content Creation",
            "script": "Welcome to our automated channel. Today we discuss how AI is changing content creation forever.",
            "tags": ["automation", "AI", "content", "future"]
        },
        {
            "title": "Building Automated YouTube Channels",
            "script": "Learn how to create self-running channels that produce content 24/7.",
            "tags": ["youtube", "automation", "python", "AI"]
        },
        {
            "title": "Dark Factory: Behind the Scenes",
            "script": "How this automated channel was built using Python and cloud services.",
            "tags": ["behindthescenes", "tech", "automation"]
        }
    ]
    
    selected = random.choice(templates)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save files
    with open(f"simple_content_{timestamp}.txt", "w") as f:
        f.write(f"TITLE: {selected['title']}\n")
        f.write(f"DATE: {datetime.now()}\n")
        f.write("=" * 40 + "\n")
        f.write(selected['script'] + "\n")
        f.write("=" * 40 + "\n")
        f.write(f"TAGS: {', '.join(selected['tags'])}\n")
    
    with open("latest_content.txt", "w") as f:
        f.write(f"TITLE: {selected['title']}\n\n")
        f.write(selected['script'])
    
    print(f"✅ Generated: {selected['title']}")
    print(f"📁 Saved to: simple_content_{timestamp}.txt")
    print(f"📁 Latest: latest_content.txt")
    
    return selected

def main():
    result = generate_simple_content()
    print("\n" + "=" * 50)
    print("🎉 SIMPLE GENERATION COMPLETE!")
    print("(Using fallback templates - Gemini API issues)")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
