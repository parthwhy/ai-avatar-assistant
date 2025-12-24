#!/usr/bin/env python3
"""
Direct test of passport PDF reading
"""

import os

def test_passport_pdf():
    """Test reading passport PDF directly."""
    
    passport_path = r"C:\Users\Parth Patel\Documents\passport.pdf"
    
    print(f"Testing passport PDF: {passport_path}")
    print(f"File exists: {os.path.exists(passport_path)}")
    
    if os.path.exists(passport_path):
        print(f"File size: {os.path.getsize(passport_path)} bytes")
        
        # Try different PDF libraries
        print("\n1. Testing with pypdf:")
        try:
            from pypdf import PdfReader
            reader = PdfReader(passport_path)
            print(f"   ✅ pypdf loaded PDF successfully")
            print(f"   📄 Number of pages: {len(reader.pages)}")
            
            if reader.is_encrypted:
                print("   🔒 PDF is encrypted")
            else:
                print("   🔓 PDF is not encrypted")
                
                # Try to extract text from first page
                if len(reader.pages) > 0:
                    page_text = reader.pages[0].extract_text()
                    print(f"   📝 First page text length: {len(page_text)} characters")
                    if page_text.strip():
                        print(f"   📋 Text preview: {page_text[:100]}...")
                    else:
                        print("   ❌ No text extracted (might be scanned image)")
                        
        except ImportError:
            print("   ❌ pypdf not available")
        except Exception as e:
            print(f"   ❌ pypdf error: {e}")
        
        print("\n2. Testing with PyPDF2:")
        try:
            import PyPDF2
            with open(passport_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                print(f"   ✅ PyPDF2 loaded PDF successfully")
                print(f"   📄 Number of pages: {len(reader.pages)}")
                
                if reader.is_encrypted:
                    print("   🔒 PDF is encrypted")
                else:
                    print("   🔓 PDF is not encrypted")
                    
                    # Try to extract text from first page
                    if len(reader.pages) > 0:
                        page_text = reader.pages[0].extract_text()
                        print(f"   📝 First page text length: {len(page_text)} characters")
                        if page_text.strip():
                            print(f"   📋 Text preview: {page_text[:100]}...")
                        else:
                            print("   ❌ No text extracted (might be scanned image)")
                            
        except ImportError:
            print("   ❌ PyPDF2 not available")
        except Exception as e:
            print(f"   ❌ PyPDF2 error: {e}")

if __name__ == "__main__":
    test_passport_pdf()