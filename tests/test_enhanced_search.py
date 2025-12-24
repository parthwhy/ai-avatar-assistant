#!/usr/bin/env python3
"""
Test Enhanced File Search
Tests the improved file search that finds partial matches.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.ai.file_analyzer import find_file, search_across_directories, analyze_document

def test_enhanced_search():
    """Test the enhanced file search functionality."""
    
    print("🔍 Testing Enhanced File Search")
    print("=" * 50)
    
    # Test search in Documents folder specifically
    documents_path = os.path.expanduser("~/Documents")
    
    print(f"Searching in: {documents_path}")
    print(f"Documents folder exists: {os.path.exists(documents_path)}")
    
    # Test various search terms
    search_terms = [
        "acceptance",
        "letter", 
        "iciss",
        "056",
        "acceptance letter"
    ]
    
    for term in search_terms:
        print(f"\n🔍 Searching for '{term}':")
        
        # Test in Documents folder
        found_path = find_file(term, documents_path)
        if found_path:
            print(f"   ✅ Found in Documents: {os.path.basename(found_path)}")
            print(f"   📁 Full path: {found_path}")
        else:
            print(f"   ❌ Not found in Documents")
        
        # Test across all directories
        found_path_all = search_across_directories(term)
        if found_path_all:
            print(f"   ✅ Found across directories: {os.path.basename(found_path_all)}")
            print(f"   📁 Full path: {found_path_all}")
        else:
            print(f"   ❌ Not found anywhere")

def test_acceptance_letter_analysis():
    """Test analyzing the acceptance letter specifically."""
    
    print("\n📄 Testing Acceptance Letter Analysis")
    print("=" * 50)
    
    # Try different variations of the search term
    search_variations = [
        "acceptance",
        "acceptance letter", 
        "letter",
        "iciss"
    ]
    
    for search_term in search_variations:
        print(f"\n📝 Analyzing with search term '{search_term}':")
        
        result = analyze_document(search_term)
        
        print(f"   Success: {result.get('success', False)}")
        
        if result.get('success'):
            print(f"   ✅ Found and analyzed: {os.path.basename(result.get('file_path', 'Unknown'))}")
            print(f"   📊 File size: {result.get('file_size', 0)} bytes")
            print(f"   📝 Content length: {result.get('content_length', 0)} characters")
            
            analysis = result.get('analysis', '')
            if analysis:
                print(f"   📋 Analysis preview: {analysis[:150]}...")
                break  # Stop after first successful analysis
            else:
                print("   ❌ No analysis generated")
        else:
            print(f"   ❌ Failed: {result.get('message', 'Unknown error')}")

def demo_search_improvements():
    """Demo the search improvements."""
    
    print("\n✨ Enhanced Search Features")
    print("=" * 50)
    
    print("🎯 Search Priority System:")
    print("   1. Exact filename match (highest priority)")
    print("   2. Exact basename match (without extension)")
    print("   3. Query contained in filename")
    print("   4. Filename contains query")
    print("   5. Word-based matching (lowest priority)")
    
    print("\n📝 Example Matches:")
    print("   Search: 'acceptance'")
    print("   ✅ Finds: 'Acceptance Letter.pdf'")
    print("   ✅ Finds: 'acceptance_report.txt'")
    print("   ✅ Finds: 'My Acceptance.docx'")
    
    print("\n🔍 Search Locations:")
    print("   • Current directory (first)")
    print("   • Desktop folder")
    print("   • Documents folder") 
    print("   • Downloads folder")
    
    print("\n🎤 Voice Commands:")
    print("   • 'Analyze document acceptance'")
    print("   • 'Analyze acceptance letter'")
    print("   • 'Analyze my letter'")

if __name__ == "__main__":
    print("🚀 Enhanced File Search Test")
    print("Testing improved partial matching for file search")
    
    test_enhanced_search()
    test_acceptance_letter_analysis()
    demo_search_improvements()
    
    print("\n🎉 Enhanced search test completed!")
    print("\n✨ Improvements:")
    print("   • Priority-based matching system")
    print("   • Partial filename matching")
    print("   • Word-based search capability")
    print("   • Case-insensitive throughout")
    print("   • Extension-agnostic searching")
    
    print("\n🎯 Now 'acceptance' should find 'Acceptance Letter.pdf'!")
    print("🎤 Try: 'Hey SAGE, analyze document acceptance'")