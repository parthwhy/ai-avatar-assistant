#!/usr/bin/env python3
"""
Simple test for acceptance letter analysis
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.ai.file_analyzer import analyze_document

def test_acceptance():
    """Test analyzing the acceptance letter."""
    
    print("📄 Testing Acceptance Letter Analysis")
    print("=" * 50)
    
    result = analyze_document("acceptance")
    
    print(f"Success: {result.get('success', False)}")
    print(f"Message: {result.get('message', 'No message')}")
    
    if result.get('file_path'):
        print(f"File found: {result.get('file_path')}")
        print(f"File size: {result.get('file_size', 0)} bytes")
        print(f"Content length: {result.get('content_length', 0)} characters")
    
    if result.get('analysis'):
        analysis = result.get('analysis')
        print(f"\nAnalysis ({len(analysis)} chars):")
        print("=" * 30)
        print(analysis)
        print("=" * 30)
    
    if result.get('error'):
        print(f"Error: {result.get('error')}")

if __name__ == "__main__":
    test_acceptance()