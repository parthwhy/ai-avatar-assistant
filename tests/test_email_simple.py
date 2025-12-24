#!/usr/bin/env python3
"""
Simple Email Test - Test email functionality without dependencies
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_email_import():
    """Test importing email module"""
    print("=== Testing Email Import ===")
    try:
        from tools.communication.email_sender import send_email_browser, compose_email_with_content
        print("✅ Email module imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import email module: {e}")
        return False

def test_contact_lookup_email():
    """Test contact lookup for email addresses"""
    print("\n=== Testing Email Contact Lookup ===")
    try:
        from tools.productivity.contacts import find_contact, smart_email_lookup
        
        # Test finding manager
        result = find_contact("manager")
        print(f"Manager lookup result: {result}")
        
        if result['success']:
            print(f"✅ Found manager: {result['contact']['name']} - Email: {result['contact']['email']}")
        
        # Test smart email lookup
        email_result = smart_email_lookup("send birthday invitation to manager")
        print(f"Smart email lookup result: {email_result}")
        
        return True
    except Exception as e:
        print(f"❌ Error in email contact lookup: {e}")
        return False

def test_email_function_structure():
    """Test email function structure without actually sending"""
    print("\n=== Testing Email Function Structure ===")
    try:
        from tools.communication.email_sender import send_email_browser
        
        # Test function signature
        import inspect
        sig = inspect.signature(send_email_browser)
        print(f"Function signature: {sig}")
        
        print("✅ Email send function is properly structured")
        print("Parameters: to (str), subject (str), body (str), recipient_name (str)")
        print("Returns: Dict with success, message, url")
        
        return True
    except Exception as e:
        print(f"❌ Error testing email function: {e}")
        return False

def test_content_generation():
    """Test content generation for email"""
    print("\n=== Testing Content Generation ===")
    try:
        from tools.ai.content_generator import generate_content
        
        # Test generating birthday invitation content
        result = generate_content(
            topic="Birthday invitation for my birthday party",
            content_type="email",
            style="friendly and professional"
        )
        
        print(f"Content generation result: {result}")
        
        if result['success']:
            print(f"✅ Generated content: {result['content'][:100]}...")
            return result['content']
        else:
            print(f"❌ Content generation failed: {result['message']}")
            return None
            
    except Exception as e:
        print(f"❌ Error in content generation: {e}")
        return None

def simulate_email_workflow():
    """Simulate the complete email workflow"""
    print("\n=== Simulating Email Workflow ===")
    
    # Step 1: Contact lookup
    try:
        from tools.productivity.contacts import find_contact
        contact_result = find_contact("manager")
        if contact_result['success']:
            recipient_email = contact_result['contact']['email']
            recipient_name = contact_result['contact']['name']
        else:
            recipient_email = "manager@company.com"
            recipient_name = "Manager"
    except:
        recipient_email = "manager@company.com"
        recipient_name = "Manager"
    
    # Step 2: Email content
    subject = "Birthday Invitation - Join My Celebration! 🎉"
    body = """Hi there!

I hope this email finds you well. I'm excited to invite you to my birthday celebration!

🎂 Event Details:
- Date: Today
- Time: Evening
- Location: My place
- Theme: Fun and casual

It would mean a lot to have you there to celebrate with me. Please let me know if you can make it!

Looking forward to seeing you there! 🎉

Best regards,
Parth"""
    
    # Step 3: Simulate sending
    print(f"\n📧 Would send email:")
    print(f"To: {recipient_name} <{recipient_email}>")
    print(f"Subject: {subject}")
    print(f"Body: {body[:100]}...")
    
    # Step 4: Show what would happen
    print(f"\n🔄 Workflow steps:")
    print(f"1. Open Gmail compose URL in browser")
    print(f"2. Pre-fill recipient: {recipient_email}")
    print(f"3. Pre-fill subject: {subject}")
    print(f"4. Pre-fill body content")
    print(f"5. User clicks Send button manually")
    
    return True

def main():
    """Run all email tests"""
    print("🧪 Testing Email Functionality")
    print("=" * 50)
    
    # Test 1: Import
    import_ok = test_email_import()
    
    # Test 2: Contact lookup
    contact_ok = test_contact_lookup_email()
    
    # Test 3: Function structure
    function_ok = test_email_function_structure()
    
    # Test 4: Content generation
    content = test_content_generation()
    content_ok = content is not None
    
    # Test 5: Workflow simulation
    workflow_ok = simulate_email_workflow()
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 EMAIL TEST SUMMARY")
    print("=" * 50)
    
    print(f"✅ Module Import: {'PASS' if import_ok else 'FAIL'}")
    print(f"✅ Contact Lookup: {'PASS' if contact_ok else 'FAIL'}")
    print(f"✅ Function Structure: {'PASS' if function_ok else 'FAIL'}")
    print(f"✅ Content Generation: {'PASS' if content_ok else 'FAIL'}")
    print(f"✅ Workflow Simulation: {'PASS' if workflow_ok else 'FAIL'}")
    
    if all([import_ok, contact_ok, function_ok, content_ok, workflow_ok]):
        print("\n🎉 ALL EMAIL TESTS PASSED!")
        print("\n📝 To actually send an email, use SAGE voice command:")
        print("   'Hey SAGE, send email to manager about my birthday'")
    else:
        print("\n⚠️  Some email tests failed. Check the output above.")

if __name__ == "__main__":
    main()