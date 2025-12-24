#!/usr/bin/env python3
"""
Demo Downloads Search GUI
Shows the GUI popup for Downloads search results.
"""

import sys
import os
import tkinter as tk
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.system.downloads_search import search_downloads

def demo_gui():
    """Demo the Downloads search GUI."""
    
    print("🖥️ Downloads Search GUI Demo")
    print("=" * 40)
    
    # Create root window (hidden)
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    print("Testing Downloads search with GUI popup...")
    
    # Test with a common search term
    result = search_downloads("exe")
    
    if result.get('success'):
        print(f"✅ Found {result.get('count', 0)} results")
        print("📱 GUI popup should have appeared with top 2 results")
        print("🖱️ Click the 'Open' buttons to open files/folders")
        
        # Keep the GUI alive for demo
        print("\n⏰ GUI will auto-close in 30 seconds")
        print("🔄 Or close manually to continue...")
        
        # Wait for GUI interaction
        root.mainloop()
    else:
        print(f"❌ Search failed: {result.get('message', 'Unknown error')}")
        root.destroy()

def demo_without_gui():
    """Demo the search functionality without showing GUI."""
    
    print("\n🔍 Downloads Search Results (No GUI)")
    print("=" * 40)
    
    # Test search without GUI
    result = search_downloads("setup")
    
    if result.get('success'):
        print(f"✅ Found {result.get('count', 0)} results for 'setup':")
        
        for i, file_info in enumerate(result.get('results', [])[:5], 1):
            print(f"   {i}. {file_info['name']}")
            print(f"      📁 {file_info['path']}")
            print(f"      📊 {file_info['size']} • {file_info['type']}")
            print()
    else:
        print(f"❌ No results: {result.get('message', 'Unknown error')}")

if __name__ == "__main__":
    print("🚀 SAGE Downloads Search GUI Demo")
    
    choice = input("\nChoose demo mode:\n1. Show GUI popup (1)\n2. Text results only (2)\nChoice: ")
    
    if choice == "1":
        demo_gui()
    else:
        demo_without_gui()
    
    print("\n🎉 Demo completed!")
    print("\n✨ Downloads Search Features:")
    print("   • Fast search in Downloads folder only")
    print("   • GUI popup with top 2 results")
    print("   • One-click file/folder opening")
    print("   • Auto-close after 30 seconds")
    print("   • Works with voice commands")
    
    print("\n🎤 Voice Commands:")
    print("   'Hey SAGE, find setup in downloads'")
    print("   'Hey SAGE, search downloads for installer'")
    print("   'Hey SAGE, find pdf in downloads'")