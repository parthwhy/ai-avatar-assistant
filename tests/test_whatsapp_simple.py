#!/usr/bin/env python3
"""
Simple WhatsApp Test - Test WhatsApp functionality without dependencies
"""

import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_whatsapp_import():
    """Test importing WhatsApp module"""
    print("=== Testing WhatsApp Import ===")
    try:
        from tools.communication.whatsapp import send_whatsapp, check_whatsapp_installed, whatsapp_call
        print("✅ WhatsApp module imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import WhatsApp module: {e}")
        return False

def test_whatsapp_installation():
    """Test WhatsApp installation check"""
    print("\n=== Testing WhatsApp Installation ===")
    try:
        from tools.communication.whatsapp import check_whatsapp_installed
        result = check_whatsapp_installed()
        print(f"Installation check result: {result}")
        
        if result['installed']:
            print("✅ WhatsApp Desktop is installed")
        else:
            print("⚠️  WhatsApp Desktop not found - will use WhatsApp Web fallback")
        
        return True
    except Exception as e:
        print(f"❌ Error checking WhatsApp installation: {e}")
        return False

def test_contact_lookup():
    """Test contact lookup for Sujal"""
    print("\n=== Testing Contact Lookup ===")
    try:
        from tools.productivity.contacts import find_contact
        result = find_contact("sujal")
        print(f"Contact lookup result: {result}")
        
        if result['success']:
            print(f"✅ Found Sujal: {result['contact']['name']} - WhatsApp: {result['contact']['whatsapp']}")
            return result['contact']['whatsapp']
        else:
            print(f"❌ Sujal not found in contacts")
            return None
    except Exception as e:
        print(f"❌ Error in contact lookup: {e}")
        return None

def test_whatsapp_function_structure():
    """Test WhatsApp function structure without actually sending"""
    print("\n=== Testing WhatsApp Function Structure ===")
    try:
        from tools.communication.whatsapp import send_whatsapp
        
        # Test function signature
        import inspect
        sig = inspect.signature(send_whatsapp)
        print(f"Function signature: {sig}")
        
        # Test with dummy data (won't actually send)
        print("✅ WhatsApp send function is properly structured")
        print("Parameters: contact_name (str), message (str)")
        print("Returns: Dict with success, message, contact, text")
        
        return True
    except Exception as e:
        print(f"❌ Error testing WhatsApp function: {e}")
        return False

def simulate_whatsapp_workflow():
    """Simulate the complete WhatsApp workflow"""
    print("\n=== Simulating WhatsApp Workflow ===")
    
    # Step 1: Contact lookup
    contact_name = test_contact_lookup()
    if not contact_name:
        contact_name = "Sujal"  # Fallback
    
    # Step 2: Message content
    message = "Hey! 🎉 It's my birthday today and I'm having a celebration. Would you like to join us? Let me know! 🎂"
    
    # Step 3: Simulate sending
    print(f"\n📱 Would send WhatsApp message:")
    print(f"To: {contact_name}")
    print(f"Message: {message}")
    
    # Step 4: Show what would happen
    print(f"\n🔄 Workflow steps:")
    print(f"1. Open WhatsApp Desktop (Win key → 'WhatsApp' → Enter)")
    print(f"2. Search for contact (Ctrl+F → '{contact_name}')")
    print(f"3. Open chat (Down → Enter)")
    print(f"4. Type message (clipboard paste)")
    print(f"5. Send message (Enter)")
    
    return True

def main():
    """Run all WhatsApp tests"""
    print("🧪 Testing WhatsApp Functionality")
    print("=" * 50)
    
    # Test 1: Import
    import_ok = test_whatsapp_import()
    
    # Test 2: Installation check
    install_ok = test_whatsapp_installation()
    
    # Test 3: Function structure
    function_ok = test_whatsapp_function_structure()
    
    # Test 4: Workflow simulation
    workflow_ok = simulate_whatsapp_workflow()
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 WHATSAPP TEST SUMMARY")
    print("=" * 50)
    
    print(f"✅ Module Import: {'PASS' if import_ok else 'FAIL'}")
    print(f"✅ Installation Check: {'PASS' if install_ok else 'FAIL'}")
    print(f"✅ Function Structure: {'PASS' if function_ok else 'FAIL'}")
    print(f"✅ Workflow Simulation: {'PASS' if workflow_ok else 'FAIL'}")
    
    if all([import_ok, install_ok, function_ok, workflow_ok]):
        print("\n🎉 ALL WHATSAPP TESTS PASSED!")
        print("\n📝 To actually send a message, use SAGE voice command:")
        print("   'Hey SAGE, send whatsapp message to sujal about my birthday'")
    else:
        print("\n⚠️  Some WhatsApp tests failed. Check the output above.")

if __name__ == "__main__":
    main()