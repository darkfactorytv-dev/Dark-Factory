#!/usr/bin/env python3
"""
Dark Factory - Content Generator
Uses Gemini API to generate YouTube content
"""
import os
import json
import google.genai as genai
from datetime import datetime

def generate_with_gemini(prompt, api_key):
    """Generate content using Gemini API"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API error: {e}")
        return None

def main():
    print("🏭 DARK FACTORY - CONTENT GENERATOR")
    print("=" * 50)
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY environment variable not set")
        print("   Set it in GitHub Secrets or locally: export GEMINI_API_KEY='your_key'")
        return 1
    
    print(f"✅ Gemini API key loaded ({len(api_key)} chars)")
    
    # Sample prompts (you can expand this)
    themes = [
        "Create a short script about emerging AI technologies for 2025",
        "Write a 2-minute YouTube video script about productivity hacks",
        "Generate content about the future of automation"
    ]
    
    import random
    selected_theme = random.choice(themes)
    
    print(f"📝 Generating content: {selected_theme[:50]}...")
    
    # Generate content
    content = generate_with_gemini(selected_theme, api_key)
    
    if content:
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"content_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"THEME: {selected_theme}\n")
            f.write(f"GENERATED: {datetime.now()}\n")
            f.write("=" * 50 + "\n")
            f.write(content)
        
        print(f"✅ Content saved to: {filename}")
        print(f"📄 Content preview: {content[:100]}...")
        
        # Also save to a standard location for the uploader
        with open("latest_content.txt", "w", encoding="utf-8") as f:
            f.write(content)
            
        return 0
    else:
        print("❌ Failed to generate content")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
