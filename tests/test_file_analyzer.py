#!/usr/bin/env python3
"""
Test File Analyzer Functionality
Tests the document analysis feature using the exact user-provided code.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.ai.file_analyzer import analyze_document, search_across_directories, find_file

def test_file_search():
    """Test the file search functionality."""
    
    print("🔍 Testing File Search Functionality")
    print("=" * 50)
    
    # Test search directories
    user_home = os.path.expanduser('~')
    search_paths = [
        os.path.join(user_home, 'Desktop'),
        os.path.join(user_home, 'Documents'),
        os.path.join(user_home, 'Downloads')
    ]
    
    print("Search directories:")
    for i, path in enumerate(search_paths, 1):
        exists = "✅" if os.path.exists(path) else "❌"
        print(f"   {i}. {exists} {path}")
    
    # Test file finding
    test_files = ["acceptance", "readme", "license", "setup"]
    
    for filename in test_files:
        print(f"\n🔍 Searching for '{filename}':")
        found_path = search_across_directories(filename)
        
        if found_path:
            print(f"   ✅ Found: {found_path}")
            print(f"   📊 Size: {os.path.getsize(found_path)} bytes")
        else:
            print(f"   ❌ Not found")

def test_document_analysis():
    """Test document analysis functionality."""
    
    print("\n📄 Testing Document Analysis")
    print("=" * 50)
    
    # Test with files that might exist
    test_documents = ["acceptance", "license", "readme", "setup"]
    
    for doc_name in test_documents:
        print(f"\n📝 Testing analysis for '{doc_name}':")
        
        result = analyze_document(doc_name)
        
        print(f"   Success: {result.get('success', False)}")
        print(f"   Message: {result.get('message', 'No message')}")
        
        if result.get('success'):
            print(f"   File: {os.path.basename(result.get('file_path', 'Unknown'))}")
            print(f"   Size: {result.get('file_size', 0)} bytes")
            print(f"   Content length: {result.get('content_length', 0)} characters")
            
            analysis = result.get('analysis', '')
            if analysis:
                print(f"   Analysis preview: {analysis[:100]}...")
            else:
                print("   No analysis generated")
        else:
            error = result.get('error', 'Unknown error')
            print(f"   Error: {error}")

def test_voice_commands():
    """Test voice command integration."""
    
    print("\n🎤 Testing Voice Command Integration")
    print("=" * 50)
    
    from core.orchestrator import get_orchestrator
    
    orchestrator = get_orchestrator()
    
    test_commands = [
        "analyze document acceptance",
        "analyze my report",
        "analyze the license file",
        "analyze pdf document"
    ]
    
    for cmd in test_commands:
        print(f"\n🎯 Command: '{cmd}'")
        
        # Test rate limit fallback
        result = orchestrator._handle_rate_limit(cmd)
        
        if result.get('fallback'):
            print("   ✅ Handled by document analysis fallback")
            response = result.get('response', '')
            if len(response) > 100:
                print(f"   Response: {response[:100]}...")
            else:
                print(f"   Response: {response}")
        else:
            print("   ℹ️ Not handled by fallback - would use AI orchestration")

def demo_analysis_features():
    """Demo the document analysis features."""
    
    print("\n✨ Document Analysis Features")
    print("=" * 50)
    
    print("📂 Supported File Types:")
    print("   • PDF files (.pdf) - Uses pypdf/PyPDF2")
    print("   • Text files (.txt, .md, .py, .csv, etc.)")
    print("   • Any text-based file format")
    
    print("\n🔍 Search Capabilities:")
    print("   • Searches Desktop, Documents, Downloads folders")
    print("   • Case-insensitive filename matching")
    print("   • Extension-agnostic (finds 'resume.pdf' when searching 'resume')")
    print("   • Recursive folder search")
    
    print("\n📄 Analysis Features:")
    print("   • AI-powered document summarization using Groq")
    print("   • Handles large documents (truncates at 20,000 characters)")
    print("   • PDF text extraction with encryption handling")
    print("   • Unicode text file support with error handling")
    
    print("\n🤖 AI Integration:")
    print("   • Uses Groq Llama 3.1 8B Instant model")
    print("   • Fast inference for quick analysis")
    print("   • Comprehensive document summaries")
    print("   • Error handling for API issues")
    
    print("\n🎤 Voice Commands:")
    print("   • 'Analyze document [name]'")
    print("   • 'Analyze my [document]'")
    print("   • 'Analyze the [document]'")
    print("   • Works even during API rate limits")

def create_test_document():
    """Create a test document for demonstration."""
    
    print("\n📝 Creating Test Document")
    print("=" * 30)
    
    documents_path = os.path.expanduser("~/Documents")
    test_file_path = os.path.join(documents_path, "sage_analysis_test.txt")
    
    test_content = """SAGE File Analysis Test Document

This document is created to test the file analysis functionality of SAGE AI Assistant.

Executive Summary:
The SAGE AI Assistant now includes advanced document analysis capabilities that can find, read, and summarize various file formats including PDFs and text files.

Key Features:
1. Intelligent File Search: Searches across Desktop, Documents, and Downloads folders
2. Multi-format Support: Handles PDF files and various text-based formats
3. AI-Powered Analysis: Uses Groq's Llama 3.1 model for comprehensive summaries
4. Voice Integration: Natural language commands for document analysis

Technical Implementation:
- Case-insensitive filename matching with extension handling
- PDF text extraction using pypdf/PyPDF2 libraries
- Unicode text file support with robust error handling
- API integration with Groq for fast AI inference
- Rate limit fallback system for reliability

Benefits:
- Quick document understanding without manual reading
- Voice-activated analysis for hands-free operation
- Support for common document formats
- Integration with existing SAGE workflow system

Conclusion:
The file analysis feature significantly enhances SAGE's productivity capabilities by enabling users to quickly understand document contents through simple voice commands.
"""
    
    try:
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        print(f"✅ Created test document: {test_file_path}")
        print("🎯 Try: 'Hey SAGE, analyze document sage analysis test'")
        
        return test_file_path
        
    except Exception as e:
        print(f"❌ Failed to create test document: {e}")
        return None

if __name__ == "__main__":
    print("🚀 SAGE File Analyzer Test Suite")
    print("Testing document analysis with user-provided code")
    
    test_file_search()
    test_document_analysis()
    test_voice_commands()
    demo_analysis_features()
    
    # Optionally create test document
    create_choice = input("\nCreate test document for demonstration? (y/n): ")
    if create_choice.lower() == 'y':
        create_test_document()
    
    print("\n🎉 File analyzer tests completed!")
    print("\n✨ Key Features:")
    print("   • Finds documents in Desktop, Documents, Downloads")
    print("   • Supports PDF and text file formats")
    print("   • AI-powered document analysis using Groq")
    print("   • Case-insensitive filename matching")
    print("   • Works during API rate limits")
    print("   • Voice command integration")
    
    print("\n🎤 Try saying:")
    print("   'Hey SAGE, analyze document acceptance'")
    print("   'Hey SAGE, analyze my report'")
    print("   'Hey SAGE, analyze the license file'")