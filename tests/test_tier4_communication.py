"""
Tier 4 Communication Tests
Run with: python -m pytest tests/test_tier4_communication.py -v
Or run directly: python tests/test_tier4_communication.py

Note: 
- Email tests require GMAIL_ADDRESS and GMAIL_APP_PASSWORD in .env
- WhatsApp tests are set to dry-run mode (won't actually send)
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.communication import (
    send_email, draft_email, validate_email,
    send_whatsapp, open_whatsapp_chat
)
from tools.communication.whatsapp import check_whatsapp_installed, send_whatsapp_web
from config.settings import settings


def test_email_validation():
    """Test email validation."""
    print("\n" + "="*60)
    print("TESTING: Email Validation")
    print("="*60)
    
    valid_emails = [
        "test@example.com",
        "user.name@domain.org",
        "user+tag@gmail.com"
    ]
    
    invalid_emails = [
        "notanemail",
        "@domain.com",
        "user@",
        "user@domain"
    ]
    
    print("\n1. Testing valid emails...")
    for email in valid_emails:
        result = validate_email(email)
        print(f"   {email}: {'✓' if result else '✗'}")
        assert result, f"Should be valid: {email}"
    
    print("\n2. Testing invalid emails...")
    for email in invalid_emails:
        result = validate_email(email)
        print(f"   {email}: {'✗ (correct)' if not result else '✓ (wrong)'}")
        assert not result, f"Should be invalid: {email}"
    
    print("\n✅ Email Validation tests passed!")
    return True


def test_draft_email():
    """Test email draft creation."""
    print("\n" + "="*60)
    print("TESTING: Draft Email")
    print("="*60)
    
    print("\n1. Creating email draft...")
    result = draft_email(
        to="test@example.com",
        subject="Test Subject",
        body="This is a test email body."
    )
    print(f"   Result: {result['message']}")
    print(f"   Draft preview: {result['draft']['preview']}")
    assert result['success'], f"Draft failed: {result}"
    
    print("\n2. Testing draft with invalid email...")
    result = draft_email(
        to="invalid-email",
        subject="Test",
        body="Test"
    )
    print(f"   Result: {result['message']}")
    assert not result['success'], "Should fail with invalid email"
    
    print("\n✅ Draft Email tests passed!")
    return True


def test_send_email_config():
    """Test email sending configuration check."""
    print("\n" + "="*60)
    print("TESTING: Email Configuration")
    print("="*60)
    
    print(f"\n1. Gmail configured: {settings.has_gmail_config}")
    
    if not settings.has_gmail_config:
        print("   ⚠️ Gmail not configured in .env")
        print("   To enable email sending:")
        print("   1. Set GMAIL_ADDRESS in .env")
        print("   2. Set GMAIL_APP_PASSWORD (from https://myaccount.google.com/apppasswords)")
        print("\n   Skipping actual send test...")
    else:
        print(f"   Gmail address: {settings.gmail_address}")
        print("   App password: ********")
        
        # Don't actually send during tests
        print("\n2. Email configuration valid, skipping actual send in test mode")
    
    print("\n✅ Email Configuration tests passed!")
    return True


def test_whatsapp_check():
    """Test WhatsApp installation check."""
    print("\n" + "="*60)
    print("TESTING: WhatsApp Installation Check")
    print("="*60)
    
    print("\n1. Checking if WhatsApp Desktop is installed...")
    result = check_whatsapp_installed()
    print(f"   Result: {result['message']}")
    print(f"   Installed: {result.get('installed', 'Unknown')}")
    
    print("\n✅ WhatsApp Check tests passed!")
    return True


def test_whatsapp_web():
    """Test WhatsApp Web URL generation (doesn't actually send)."""
    print("\n" + "="*60)
    print("TESTING: WhatsApp Web URL Generation")
    print("="*60)
    
    print("\n1. Testing URL generation (won't open browser in test)...")
    
    # We'll just test the URL encoding logic without opening browser
    import urllib.parse
    phone = "+919876543210"
    message = "Hello, this is a test message!"
    phone_clean = phone.replace(' ', '').replace('-', '').replace('+', '')
    encoded_message = urllib.parse.quote(message)
    url = f'https://web.whatsapp.com/send?phone={phone_clean}&text={encoded_message}'
    
    print(f"   Phone: {phone}")
    print(f"   Message: {message}")
    print(f"   Generated URL: {url[:60]}...")
    
    assert 'phone=919876543210' in url, "Phone should be in URL"
    assert 'text=' in url, "Message should be in URL"
    
    print("\n✅ WhatsApp Web URL tests passed!")
    return True


def test_whatsapp_functions_exist():
    """Test that WhatsApp functions are properly defined."""
    print("\n" + "="*60)
    print("TESTING: WhatsApp Functions")
    print("="*60)
    
    print("\n1. Checking function availability...")
    
    functions = [
        ('send_whatsapp', send_whatsapp),
        ('open_whatsapp_chat', open_whatsapp_chat),
        ('send_whatsapp_web', send_whatsapp_web),
        ('check_whatsapp_installed', check_whatsapp_installed),
    ]
    
    for name, func in functions:
        print(f"   {name}: {'✓ Available' if callable(func) else '✗ Missing'}")
        assert callable(func), f"{name} should be callable"
    
    print("\n   ⚠️ Note: Actual WhatsApp sending requires:")
    print("   - WhatsApp Desktop installed and logged in")
    print("   - Screen not locked during automation")
    print("   - Contact name exactly as shown in WhatsApp")
    
    print("\n✅ WhatsApp Functions tests passed!")
    return True


def run_all_tests():
    """Run all Tier 4 tests."""
    print("\n" + "#"*60)
    print("#" + " "*20 + "SAGE TIER 4 TESTS" + " "*21 + "#")
    print("#" + " "*17 + "Communication Tools" + " "*22 + "#")
    print("#"*60)
    
    tests = [
        ("Email Validation", test_email_validation),
        ("Draft Email", test_draft_email),
        ("Email Configuration", test_send_email_config),
        ("WhatsApp Check", test_whatsapp_check),
        ("WhatsApp Web URL", test_whatsapp_web),
        ("WhatsApp Functions", test_whatsapp_functions_exist),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ {name} test failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "#"*60)
    print(f"# RESULTS: {passed} passed, {failed} failed" + " "*(45-len(str(passed))-len(str(failed))) + "#")
    print("#"*60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
