#!/usr/bin/env python3
"""
File Search Demo
Demonstrates the new file search capabilities in SAGE.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.system.file_search import search_file, search_files_by_type
from core.orchestrator import get_orchestrator

def demo_file_search():
    """Demo the file search functionality."""
    
    print("🔍 SAGE File Search Demo")
    print("=" * 50)
    
    print("\n1️⃣ Search for specific files:")
    print("   Voice command: 'Find my config file'")
    
    result = search_file("config", max_results=3)
    if result.get('success') and result.get('results'):
        print(f"   ✅ Found {len(result['results'])} files:")
        for i, file_info in enumerate(result['results'], 1):
            print(f"      {i}. {file_info['name']}")
            print(f"         📁 {file_info['directory']}")
            print(f"         📊 {file_info['size']} | {file_info['type']}")
    else:
        print("   ❌ No config files found")
    
    print("\n2️⃣ Search by file type:")
    print("   Voice command: 'Find all my documents'")
    
    result = search_files_by_type("document", max_results=3)
    if result.get('success') and result.get('results'):
        print(f"   ✅ Found {len(result['results'])} documents:")
        for i, file_info in enumerate(result['results'], 1):
            print(f"      {i}. {file_info['name']}")
            print(f"         📁 {file_info['directory']}")
            print(f"         📊 {file_info['size']}")
    else:
        print("   ❌ No documents found")
    
    print("\n3️⃣ Search for images:")
    print("   Voice command: 'Find my photos'")
    
    result = search_files_by_type("image", max_results=3)
    if result.get('success') and result.get('results'):
        print(f"   ✅ Found {len(result['results'])} images:")
        for i, file_info in enumerate(result['results'], 1):
            print(f"      {i}. {file_info['name']}")
            print(f"         📁 {file_info['directory']}")
            print(f"         📊 {file_info['size']}")
    else:
        print("   ❌ No images found")

def demo_voice_commands():
    """Demo voice commands for file search."""
    
    print("\n🎤 Voice Commands for File Search")
    print("=" * 50)
    
    commands = [
        ("Find my resume", "Searches for files containing 'resume'"),
        ("Search for config file", "Searches for configuration files"),
        ("Find all my documents", "Finds all document files (.pdf, .doc, .txt)"),
        ("Find my photos", "Finds all image files (.jpg, .png, .gif)"),
        ("Search for video files", "Finds all video files (.mp4, .avi, .mkv)"),
        ("Open location of config.txt", "Opens folder containing config.txt"),
        ("Find executable files", "Finds all .exe and .msi files")
    ]
    
    for cmd, description in commands:
        print(f"   🎯 '{cmd}'")
        print(f"      → {description}")
        print()

def demo_rate_limit_fallback():
    """Demo rate limit fallback for file search."""
    
    print("\n🔄 Rate Limit Fallback Demo")
    print("=" * 50)
    
    orchestrator = get_orchestrator()
    
    # Test commands that should work with fallback
    test_commands = [
        "search for config file",
        "find readme",
        "locate notepad"
    ]
    
    for cmd in test_commands:
        print(f"\n🔍 Testing fallback: '{cmd}'")
        result = orchestrator._handle_rate_limit(cmd)
        
        if result.get('fallback'):
            print("   ✅ Handled by fallback system")
            response = result.get('response', '')
            if len(response) > 100:
                print(f"   📝 {response[:100]}...")
            else:
                print(f"   📝 {response}")
        else:
            print("   ℹ️ Would use AI orchestration")

if __name__ == "__main__":
    print("🚀 SAGE File Search Capabilities")
    
    demo_file_search()
    demo_voice_commands()
    demo_rate_limit_fallback()
    
    print("\n🎉 File Search Demo Complete!")
    print("\n✨ Key Features:")
    print("   • Fast file search across common locations")
    print("   • Search by filename or file type")
    print("   • Open file locations in Explorer")
    print("   • Works even during API rate limits")
    print("   • Natural language voice commands")
    print("   • Supports documents, images, videos, executables")
    
    print("\n🎤 Try saying:")
    print("   'Hey SAGE, find my resume file'")
    print("   'Hey SAGE, search for all my photos'")
    print("   'Hey SAGE, open location of config.txt'")