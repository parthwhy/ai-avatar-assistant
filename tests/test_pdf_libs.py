#!/usr/bin/env python3
"""
Test PDF Libraries
"""

print("Testing PDF library imports...")

try:
    from pypdf import PdfReader
    print("✅ pypdf imported successfully")
    PdfReader_class = PdfReader
except ImportError as e:
    print(f"❌ pypdf import failed: {e}")
    try:
        import PyPDF2
        print("✅ PyPDF2 available as fallback")
        PdfReader_class = PyPDF2.PdfReader
    except ImportError as e2:
        print(f"❌ PyPDF2 also failed: {e2}")
        PdfReader_class = None

if PdfReader_class:
    print(f"✅ Using PDF reader: {PdfReader_class}")
else:
    print("❌ No PDF reader available")

# Test the actual file analyzer import
try:
    from tools.ai.file_analyzer import analyze_document
    print("✅ File analyzer imported successfully")
    
    # Test passport analysis
    print("\n📄 Testing passport analysis...")
    result = analyze_document('passport')
    print(f"Success: {result.get('success')}")
    print(f"Message: {result.get('message')}")
    if result.get('error'):
        print(f"Error: {result.get('error')}")
        
except Exception as e:
    print(f"❌ File analyzer error: {e}")