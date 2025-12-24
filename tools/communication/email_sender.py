"""
Email Sender Tool - Browser Only
Send emails via Gmail in browser using PyAutoGUI automation.
Integrates with contacts database for easy recipient lookup.
"""

import re
import time
import webbrowser
import urllib.parse
from typing import Dict, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Try to import pyautogui for browser automation
try:
    import pyautogui
    import pyperclip
    AUTOMATION_AVAILABLE = True
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
except ImportError:
    AUTOMATION_AVAILABLE = False


def validate_email(email: str) -> bool:
    """Validate email address format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def lookup_contact_email(recipient: str) -> Dict[str, any]:
    """
    Look up email address from contacts database.
    
    Args:
        recipient: Name or role (e.g., 'manager', 'sujal', 'hr')
    
    Returns:
        Dictionary with email and contact info
    """
    try:
        from tools.productivity.contacts import find_contact
        result = find_contact(recipient)
        
        if result['success']:
            contact = result['contact']
            return {
                'success': True,
                'email': contact.get('email', ''),
                'name': contact.get('name', recipient),
                'role': contact.get('role', '')
            }
        else:
            return {
                'success': False,
                'message': result['message']
            }
    except Exception as e:
        return {
            'success': False,
            'message': f'Contact lookup failed: {str(e)}'
        }


def send_email_browser(
    to: str = None,
    subject: str = None,
    body: str = None,
    recipient_name: str = None,
    send_immediately: bool = False
) -> Dict[str, any]:
    """
    Send email using Gmail in browser.
    
    Args:
        to: Recipient email address (optional if recipient_name provided)
        subject: Email subject (will ask if not provided)
        body: Email body (will ask if not provided)
        recipient_name: Contact name/role to look up email (e.g., 'manager')
        send_immediately: If True, sends immediately. If False, opens for review.
    
    Returns:
        Dictionary with result or request for missing info.
    """
    if not AUTOMATION_AVAILABLE:
        return {
            'success': False,
            'message': 'PyAutoGUI not available. Install with: pip install pyautogui pyperclip'
        }
    
    # If recipient_name provided, look up email from contacts
    if recipient_name and not to:
        contact_result = lookup_contact_email(recipient_name)
        if contact_result['success']:
            to = contact_result['email']
            print(f"Found email for {recipient_name}: {to}")
        else:
            return {
                'success': False,
                'needs_info': True,
                'missing': 'recipient',
                'message': f"I couldn't find {recipient_name} in contacts. Who should I send this email to?",
                'response': f"I couldn't find {recipient_name} in contacts. Please provide the email address."
            }
    
    # Check if we have recipient
    if not to:
        return {
            'success': False,
            'needs_info': True,
            'missing': 'recipient',
            'message': 'Who should I send this email to?',
            'response': 'Who should I send this email to? Please provide a name or email address.'
        }
    
    # Validate email if provided directly
    if to and not validate_email(to):
        # Maybe it's a contact name, try lookup
        # Clean up common patterns like "HR email", "manager's email", etc.
        clean_name = to.lower().replace(' email', '').replace("'s email", '').replace(' address', '').strip()
        contact_result = lookup_contact_email(clean_name)
        if contact_result['success']:
            to = contact_result['email']
            print(f"Found email for {clean_name}: {to}")
        else:
            # Try original value too
            contact_result = lookup_contact_email(to)
            if contact_result['success']:
                to = contact_result['email']
            else:
                return {
                    'success': False,
                    'needs_info': True,
                    'missing': 'valid_email',
                    'message': f"'{to}' is not a valid email and not found in contacts.",
                    'response': f"I couldn't find '{to}' in contacts. Please provide a valid email address."
                }
    
    # Check if we have subject
    if not subject:
        return {
            'success': False,
            'needs_info': True,
            'missing': 'subject',
            'message': 'What is the email about?',
            'response': 'What should be the subject of this email?'
        }
    
    # Check if we have body
    if not body:
        return {
            'success': False,
            'needs_info': True,
            'missing': 'body',
            'message': 'What should the email say?',
            'response': 'What would you like to say in this email?'
        }
    
    try:
        print(f"Opening Gmail compose for {to}...")
        
        # URL-encode subject and body for Gmail compose URL
        encoded_to = urllib.parse.quote(to)
        encoded_subject = urllib.parse.quote(subject)
        encoded_body = urllib.parse.quote(body)
        
        # Gmail compose URL with all fields pre-filled
        compose_url = f'https://mail.google.com/mail/?view=cm&to={encoded_to}&su={encoded_subject}&body={encoded_body}'
        
        webbrowser.open(compose_url)
        
        # Wait for browser to open
        time.sleep(2)
        
        if send_immediately:
            print("Sending email...")
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'enter')
            time.sleep(1)
            
            return {
                'success': True,
                'message': f'Email sent to {to}',
                'to': to,
                'subject': subject,
                'method': 'browser'
            }
        else:
            return {
                'success': True,
                'message': f'Email composed for {to}. Review and click Send.',
                'to': to,
                'subject': subject,
                'method': 'browser',
                'response': f'I\'ve opened Gmail with your email to {to}. Please review and click Send.'
            }
        
    except pyautogui.FailSafeException:
        return {
            'success': False,
            'message': 'Automation aborted (mouse moved to corner).'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to compose email: {str(e)}'
        }


def send_email(
    to: str = None,
    subject: str = None,
    body: str = None,
    recipient_name: str = None
) -> Dict[str, any]:
    """
    Main email function - uses browser automation.
    Alias for send_email_browser for backward compatibility.
    """
    return send_email_browser(
        to=to,
        subject=subject,
        body=body,
        recipient_name=recipient_name,
        send_immediately=False
    )


def quick_email(to: str, message: str) -> Dict[str, any]:
    """
    Quick email - auto-generates subject from message.
    
    Args:
        to: Recipient email or contact name
        message: Email message
    
    Returns:
        Dictionary with result.
    """
    # Generate subject from first line
    first_line = message.split('\n')[0][:50]
    subject = first_line if len(first_line) > 5 else "Message from SAGE"
    
    return send_email_browser(to=to, subject=subject, body=message)


def compose_email_with_content(
    recipient: str,
    content: str,
    subject: str = None
) -> Dict[str, any]:
    """
    Compose email with pre-generated content.
    
    Args:
        recipient: Contact name or email
        content: Email body content
        subject: Optional subject (auto-generated if not provided)
    
    Returns:
        Dictionary with result.
    """
    # Look up recipient if it's a name
    to_email = recipient
    if not validate_email(recipient):
        contact_result = lookup_contact_email(recipient)
        if contact_result['success']:
            to_email = contact_result['email']
        else:
            return contact_result
    
    # Auto-generate subject if not provided
    if not subject:
        first_line = content.split('\n')[0][:50]
        subject = first_line if len(first_line) > 5 else "Message"
    
    return send_email_browser(to=to_email, subject=subject, body=content)