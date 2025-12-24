#!/usr/bin/env python3
"""
Test Downloads Search Functionality
Tests the focused Downloads folder search with GUI options.
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.system.downloads_search import search_downloads

def test_downloads_search():
    """Test the Downloads folder search functionality."""
    
    print("📥 Testing Downloads Search Functionality")
    print("=" * 50)
    
    downloads_path = os.path.expanduser("~/Downloads")
    print(f"Downloads path: {downloads_path}")
    print(f"Downloads exists: {os.path.exists(downloads_path)}")
    
    if not os.path.exists(downloads_path):
        print("❌ Downloads folder not found - creating test scenario")
        return
    
    # List some files in Downloads for testing
    try:
        files_in_downloads = os.listdir(downloads_path)[:10]
        print(f"\nFiles in Downloads (first 10):")
        for i, filename in enumerate(files_in_downloads, 1):
            print(f"   {i}. {filename}")
    except PermissionError:
        print("❌ Cannot access Downloads folder")
        return
    
    # Test searches
    test_terms = ["setup", "download", "exe", "pdf", "zip"]
    
    for term in test_terms:
        print(f"\n🔍 Testing search for '{term}' in Downloads:")
        result = search_downloads(term)
        
        print(f"   Success: {result.get('success', False)}")
        print(f"   Count: {result.get('count', 0)}")
        print(f"   GUI shown: {result.get('gui_shown', False)}")
        
        if result.get('results'):
            print(f"   Results:")
            for i, file_info in enumerate(result['results'][:3], 1):
                print(f"      {i}. {file_info['name']} ({file_info['size']})")
        
        # Small delay between searches
        time.sleep(1)

def test_voice_commands():
    """Test voice command integration."""
    
    print("\n🎤 Testing Voice Command Integration")
    print("=" * 50)
    
    from core.orchestrator import get_orchestrator
    
    orchestrator = get_orchestrator()
    
    test_commands = [
        "find setup in downloads",
        "search downloads for pdf",
        "find in downloads",  # Should ask for filename
        "search downloads for exe"
    ]
    
    for cmd in test_commands:
        print(f"\n🎯 Command: '{cmd}'")
        
        # Test rate limit fallback
        result = orchestrator._handle_rate_limit(cmd)
        
        if result.get('fallback'):
            print("   ✅ Handled by Downloads search fallback")
            response = result.get('response', '')
            print(f"   Response: {response[:80]}...")
        else:
            print("   ℹ️ Not handled by fallback - would use AI orchestration")

def demo_gui_features():
    """Demo the GUI features (without actually showing GUI)."""
    
    print("\n🖥️ GUI Features Demo")
    print("=" * 50)
    
    print("📱 Downloads Search GUI Features:")
    print("   ┌─────────────────────────────────────┐")
    print("   │ Found in Downloads: setup           │")
    print("   ├─────────────────────────────────────┤")
    print("   │ 1. setup.exe                        │")
    print("   │    File • 2.5 MB        [📂 Open]  │")
    print("   ├─────────────────────────────────────┤")
    print("   │ 2. setup_backup.exe                 │")
    print("   │    File • 1.8 MB        [📂 Open]  │")
    print("   ├─────────────────────────────────────┤")
    print("   │                [Close]              │")
    print("   └─────────────────────────────────────┘")
    
    print("\n✨ GUI Features:")
    print("   • Shows only top 2 results")
    print("   • Clickable 'Open' buttons for each file")
    print("   • File type and size information")
    print("   • Auto-closes after 30 seconds")
    print("   • Opens files with default applications")
    print("   • Opens folders in Windows Explorer")
    
    print("\n🎯 User Experience:")
    print("   1. Say 'find setup in downloads'")
    print("   2. GUI popup appears with top 2 matches")
    print("   3. Click 'Open' button to open file/folder")
    print("   4. Popup closes automatically")

def demo_voice_commands():
    """Demo voice commands for Downloads search."""
    
    print("\n🎤 Voice Commands for Downloads Search")
    print("=" * 50)
    
    commands = [
        ("Find setup in downloads", "Searches Downloads for 'setup' files"),
        ("Search downloads for pdf", "Finds PDF files in Downloads"),
        ("Find exe in downloads", "Looks for executable files"),
        ("Search downloads for zip", "Finds archive files"),
        ("Find installer in downloads", "Searches for installer files"),
    ]
    
    for cmd, description in commands:
        print(f"   🎯 '{cmd}'")
        print(f"      → {description}")
        print(f"      → Shows GUI with top 2 results")
        print(f"      → Click to open files directly")
        print()

if __name__ == "__main__":
    print("🚀 SAGE Downloads Search Test Suite")
    print("Testing focused Downloads folder search with GUI")
    
    test_downloads_search()
    test_voice_commands()
    demo_gui_features()
    demo_voice_commands()
    
    print("\n🎉 Downloads search tests completed!")
    print("\n✨ Key Features:")
    print("   • Searches only Downloads folder (fast & focused)")
    print("   • Shows GUI popup with top 2 results")
    print("   • Clickable buttons to open files/folders")
    print("   • Works during API rate limits")
    print("   • Sorts by newest files first")
    print("   • Auto-closes GUI after 30 seconds")
    
    print("\n🎤 Try saying:")
    print("   'Hey SAGE, find setup in downloads'")
    print("   'Hey SAGE, search downloads for pdf'")
    print("   'Hey SAGE, find installer in downloads'")