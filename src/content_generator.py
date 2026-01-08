#!/usr/bin/env python3
"""
Dark Factory - Real Content Generator
Generates actual YouTube content using Gemini API
"""
import sys
import os
import json
from datetime import datetime

# Import credentials from our embedded system
sys.path.append(os.path.dirname(__file__))
from darker_factory import decode_credentials

import google.genai as genai

def generate_youtube_script():
    """Generate a complete YouTube video script"""
    print("🎬 DARK FACTORY CONTENT GENERATOR")
    print("=" * 60)
    
    # Get credentials
    gemini_key, _ = decode_credentials()
    
    if not gemini_key:
        print("❌ No Gemini API key found")
        return None
    
    try:
        # Configure Gemini
        genai.configure(api_key=gemini_key)
        
        # Use Gemini 2.0 Flash (fast and capable)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # YouTube video topics for automation/tech niche
        topics = [
            "Create a 3-minute YouTube script about AI content automation",
            "Write a short video script about building automated YouTube channels",
            "Generate content about the future of automated content creation",
            "Create a script about Python automation for social media"
        ]
        
        import random
        selected_topic = random.choice(topics)
        
        print(f"📝 Topic: {selected_topic}")
        print("⏳ Generating with Gemini...")
        
        # Generate script
        prompt = f"""
        Create a complete YouTube video script for a short video (2-3 minutes).
        Topic: {selected_topic}
        
        Format:
        1. Catchy title
        2. Hook (first 15 seconds to grab attention)
        3. Main content (3-4 key points)
        4. Call to action
        5. Suggested tags
        
        Make it engaging and suitable for an automated tech channel.
        """
        
        response = model.generate_content(prompt)
        script = response.text
        
        # Generate title separately
        title_prompt = f"Generate a catchy YouTube title for a video about: {selected_topic}"
        title_response = model.generate_content(title_prompt)
        title = title_response.text.strip().replace('"', '')
        
        print(f"✅ Generated: '{title}'")
        print(f"📄 Script length: {len(script)} characters")
        
        # Save with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_files = []
        
        # Save full script
        script_filename = f"youtube_script_{timestamp}.txt"
        with open(script_filename, "w", encoding="utf-8") as f:
            f.write(f"TITLE: {title}\n")
            f.write(f"TOPIC: {selected_topic}\n")
            f.write(f"GENERATED: {datetime.now()}\n")
            f.write("=" * 50 + "\n")
            f.write(script)
        
        output_files.append(script_filename)
        
        # Save as latest content
        with open("latest_content.txt", "w", encoding="utf-8") as f:
            f.write(f"TITLE: {title}\n\n")
            f.write(script)
        
        # Save metadata
        metadata = {
            "title": title,
            "topic": selected_topic,
            "generated_at": datetime.now().isoformat(),
            "script_length": len(script),
            "model": "gemini-2.0-flash-exp"
        }
        
        with open(f"metadata_{timestamp}.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        
        output_files.append(f"metadata_{timestamp}.json")
        
        print(f"💾 Saved to: {', '.join(output_files)}")
        print(f"📁 Also saved as: latest_content.txt")
        
        return {
            "title": title,
            "script": script,
            "files": output_files
        }
        
    except Exception as e:
        print(f"❌ Generation error: {type(e).__name__}: {e}")
        return None

def main():
    result = generate_youtube_script()
    
    if result:
        print("\n" + "=" * 60)
        print("🎉 CONTENT GENERATION SUCCESSFUL!")
        print(f"Title: {result['title'][:50]}...")
        print(f"Files created: {len(result['files'])}")
        print("=" * 60)
        return 0
    else:
        print("\n❌ CONTENT GENERATION FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
