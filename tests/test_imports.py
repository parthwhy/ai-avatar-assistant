#!/usr/bin/env python3
"""
Test imports
"""

print("Testing PDF library imports...")

try:
    import pypdf
    print("✅ pypdf module imported")
    from pypdf import PdfReader
    print("✅ PdfReader imported from pypdf")
except Exception as e:
    print(f"❌ pypdf error: {e}")

try:
    import PyPDF2
    print("✅ PyPDF2 module imported")
except Exception as e:
    print(f"❌ PyPDF2 error: {e}")

# Test the file analyzer
print("\nTesting file analyzer...")
try:
    from tools.ai.file_analyzer import analyze_document
    print("✅ File analyzer imported")
    
    # Test with passport
    print("Analyzing passport...")
    result = analyze_document('passport')
    print(f"Success: {result.get('success')}")
    if not result.get('success'):
        print(f"Error: {result.get('error', result.get('message'))}")
    else:
        analysis = result.get('analysis', '')
        print(f"Analysis length: {len(analysis)} chars")
        if analysis:
            print(f"Preview: {analysis[:100]}...")
            
except Exception as e:
    print(f"❌ File analyzer error: {e}")
    import traceback
    traceback.print_exc()