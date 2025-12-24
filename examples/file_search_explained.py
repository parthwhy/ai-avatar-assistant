#!/usr/bin/env python3
"""
File Search Functionality Explained
Comprehensive guide to how SAGE's file search works and what it can find.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.system.file_search import search_file, search_files_by_type

def explain_search_locations():
    """Explain where the file search looks for files."""
    
    print("🔍 SAGE File Search - How It Works")
    print("=" * 50)
    
    print("📂 Default Search Locations:")
    print("   When you don't specify a path, SAGE searches:")
    
    # Show actual paths on this system
    search_paths = [
        os.path.expanduser("~"),  # User home directory
        "C:\\Users",  # All users
        "C:\\Program Files",  # Program files
        "C:\\Program Files (x86)",  # 32-bit programs
        "D:\\" if os.path.exists("D:\\") else None,  # D drive if exists
    ]
    search_paths = [p for p in search_paths if p and os.path.exists(p)]
    
    for i, path in enumerate(search_paths, 1):
        exists = "✅" if os.path.exists(path) else "❌"
        print(f"   {i}. {exists} {path}")
        
        # Show what's typically in each location
        if "Users" in path and path.endswith("Users"):
            print("      → All user profiles and their files")
        elif path == os.path.expanduser("~"):
            print("      → Your personal files (Documents, Downloads, Desktop, etc.)")
        elif "Program Files" in path:
            print("      → Installed applications and their files")
        elif path.startswith("D:"):
            print("      → Secondary drive (if available)")
    
    print(f"\n📊 Total searchable locations: {len(search_paths)}")

def explain_search_methods():
    """Explain the different search methods used."""
    
    print("\n🔧 Search Methods Used:")
    print("=" * 30)
    
    print("1️⃣ Glob Pattern Matching (Primary Method)")
    print("   • **/*filename* - Files containing the name anywhere")
    print("   • **/filename - Exact filename matches")
    print("   • **/filename.* - Filename with any extension")
    print("   • Recursive search through all subdirectories")
    print("   • Fast and comprehensive")
    
    print("\n2️⃣ Windows 'where' Command (Backup Method)")
    print("   • Used for executable files when glob finds few results")
    print("   • Searches system PATH for .exe files")
    print("   • Good for finding installed programs")
    
    print("\n3️⃣ File Type Categories")
    print("   • Documents: .doc, .docx, .pdf, .txt, .rtf")
    print("   • Images: .jpg, .jpeg, .png, .gif, .bmp, .tiff")
    print("   • Videos: .mp4, .avi, .mkv, .mov, .wmv, .flv")
    print("   • Audio: .mp3, .wav, .flac, .aac, .ogg, .wma")
    print("   • Archives: .zip, .rar, .7z, .tar, .gz")
    print("   • Executables: .exe, .msi, .bat, .cmd")

def explain_search_capabilities():
    """Explain what the search can and cannot do."""
    
    print("\n✅ What SAGE File Search CAN Do:")
    print("=" * 40)
    
    capabilities = [
        "Find files by partial name (e.g., 'config' finds 'config.txt', 'myconfig.ini')",
        "Search by file type (e.g., 'find all documents')",
        "Search entire drives recursively",
        "Find files in user directories, program files, and additional drives",
        "Show file size, modification date, and full path",
        "Open file locations in Windows Explorer",
        "Handle permission errors gracefully",
        "Work even during API rate limits (fallback mode)",
        "Search for both files and folders",
        "Find files with or without extensions"
    ]
    
    for i, capability in enumerate(capabilities, 1):
        print(f"   {i:2d}. {capability}")
    
    print("\n❌ What SAGE File Search CANNOT Do:")
    print("=" * 40)
    
    limitations = [
        "Search inside file contents (only searches filenames)",
        "Access system-protected directories without permissions",
        "Search network drives (only local drives)",
        "Find files in hidden system folders (some restrictions)",
        "Search based on file creation date or other metadata",
        "Perform fuzzy matching (needs partial filename match)",
        "Search compressed archives contents",
        "Index files for faster future searches"
    ]
    
    for i, limitation in enumerate(limitations, 1):
        print(f"   {i:2d}. {limitation}")

def demo_search_examples():
    """Show practical search examples."""
    
    print("\n🎯 Practical Search Examples:")
    print("=" * 40)
    
    examples = [
        {
            "command": "Find my resume",
            "searches_for": "Files containing 'resume' anywhere in the name",
            "finds": "resume.pdf, my_resume.docx, resume_2024.txt"
        },
        {
            "command": "Search for config file", 
            "searches_for": "Files containing 'config' in the name",
            "finds": "config.ini, app_config.json, config.txt"
        },
        {
            "command": "Find all my documents",
            "searches_for": "All document file types in common locations",
            "finds": ".pdf, .doc, .docx, .txt files in Documents, Downloads, etc."
        },
        {
            "command": "Find chrome",
            "searches_for": "Files/folders containing 'chrome'",
            "finds": "chrome.exe, Chrome folder, chrome shortcuts"
        },
        {
            "command": "Find my photos",
            "searches_for": "All image file types",
            "finds": ".jpg, .png, .gif files in Pictures, Downloads, etc."
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}️⃣ Voice Command: '{example['command']}'")
        print(f"   🔍 Searches for: {example['searches_for']}")
        print(f"   📁 Typically finds: {example['finds']}")

def test_current_system():
    """Test the search on the current system."""
    
    print("\n🧪 Testing on Your Current System:")
    print("=" * 40)
    
    # Test common searches
    test_searches = [
        ("notepad", "Common Windows application"),
        ("config", "Configuration files"),
        ("readme", "Documentation files"),
        ("chrome", "Browser-related files")
    ]
    
    for filename, description in test_searches:
        print(f"\n🔍 Searching for '{filename}' ({description}):")
        result = search_file(filename, max_results=3)
        
        if result.get('success') and result.get('results'):
            print(f"   ✅ Found {len(result['results'])} files:")
            for file_info in result['results'][:2]:
                print(f"      📄 {file_info['name']}")
                print(f"         📁 {file_info['directory'][:50]}...")
        else:
            print(f"   ❌ No files found")
    
    # Test file type search
    print(f"\n📄 Searching for document files:")
    result = search_files_by_type("document", max_results=3)
    
    if result.get('success') and result.get('results'):
        print(f"   ✅ Found {len(result['results'])} documents:")
        for file_info in result['results'][:2]:
            print(f"      📄 {file_info['name']} ({file_info['size']})")
    else:
        print(f"   ❌ No documents found")

if __name__ == "__main__":
    print("📚 Complete Guide to SAGE File Search")
    
    explain_search_locations()
    explain_search_methods()
    explain_search_capabilities()
    demo_search_examples()
    test_current_system()
    
    print("\n🎉 File Search Guide Complete!")
    
    print("\n💡 Key Points:")
    print("   • Searches your entire system by default")
    print("   • Finds files by partial name matching")
    print("   • Supports file type categories")
    print("   • Works even during API rate limits")
    print("   • Shows detailed file information")
    print("   • Can open file locations")
    
    print("\n🎤 Voice Commands to Try:")
    print("   'Hey SAGE, find my resume file'")
    print("   'Hey SAGE, search for config files'")
    print("   'Hey SAGE, find all my documents'")
    print("   'Hey SAGE, find chrome'")
    print("   'Hey SAGE, open location of config.txt'")