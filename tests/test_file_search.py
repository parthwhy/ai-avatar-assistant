#!/usr/bin/env python3
"""
Test File Search Functionality
Tests the new file search tools and integration.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.system.file_search import search_file, search_files_by_type, open_file_location
from core.orchestrator import get_orchestrator

def test_file_search_functions():
    """Test the file search functions directly."""
    
    print("🔍 Testing File Search Functions")
    print("=" * 40)
    
    # Test 1: Search for common files
    test_files = ["notepad", "chrome", "config", "readme"]
    
    for filename in test_files:
        print(f"\n🔍 Searching for: '{filename}'")
        result = search_file(filename, max_results=3)
        
        print(f"   Success: {result.get('success', False)}")
        print(f"   Count: {result.get('count', 0)}")
        
        if result.get('results'):
            for i, file_info in enumerate(result['results'][:2], 1):
                print(f"   {i}. {file_info['name']} ({file_info['type']})")
                print(f"      Path: {file_info['path'][:60]}...")
        else:
            print(f"   No results found")

def test_file_type_search():
    """Test searching by file type."""
    
    print("\n📁 Testing File Type Search")
    print("=" * 40)
    
    file_types = ["document", "image", "executable"]
    
    for file_type in file_types:
        print(f"\n📄 Searching for: {file_type} files")
        result = search_files_by_type(file_type, max_results=3)
        
        print(f"   Success: {result.get('success', False)}")
        print(f"   Count: {result.get('count', 0)}")
        
        if result.get('results'):
            for i, file_info in enumerate(result['results'][:2], 1):
                print(f"   {i}. {file_info['name']} ({file_info['size']})")
        else:
            print(f"   No {file_type} files found")

def test_orchestrator_integration():
    """Test file search through the orchestrator."""
    
    print("\n🤖 Testing Orchestrator Integration")
    print("=" * 40)
    
    orchestrator = get_orchestrator()
    
    test_commands = [
        "find notepad",
        "search for config file",
        "find all my documents",
        "search for image files"
    ]
    
    for cmd in test_commands:
        print(f"\n🎯 Command: '{cmd}'")
        
        try:
            # Test rate limit fallback first
            result = orchestrator._handle_rate_limit(cmd)
            
            if result.get('fallback'):
                print("   ✅ Fallback handled file search")
                print(f"   Response: {result.get('response', 'No response')[:80]}...")
            else:
                print("   ℹ️ Not handled by fallback - would use AI orchestration")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_file_location_opening():
    """Test opening file locations."""
    
    print("\n📂 Testing File Location Opening")
    print("=" * 40)
    
    # Find a file first
    result = search_file("notepad", max_results=1)
    
    if result.get('success') and result.get('results'):
        filepath = result['results'][0]['path']
        print(f"Found file: {filepath}")
        
        # Test opening location (but don't actually open to avoid disruption)
        print("Would open file location (skipped for test)")
        print("✅ File location function available")
    else:
        print("No test file found for location opening test")

if __name__ == "__main__":
    print("🚀 SAGE File Search Test Suite")
    print("Testing file search functionality")
    
    test_file_search_functions()
    test_file_type_search()
    test_orchestrator_integration()
    test_file_location_opening()
    
    print("\n🎉 File search tests completed!")
    print("\nℹ️  File search supports:")
    print("   • Search by filename: 'find my resume'")
    print("   • Search by type: 'find all documents'")
    print("   • Open file location: 'open location of config.txt'")
    print("   • Rate limit fallbacks for common searches")
    print("   • Multiple search methods (glob, Windows search)")