"""
WhatsApp Automation Tool
Send WhatsApp messages using PyAutoGUI automation.
"""

import time
import pyautogui
import subprocess
from typing import Dict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


# PyAutoGUI safety settings
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.3  # Pause between actions


def open_whatsapp_chat(contact_name: str) -> Dict[str, any]:
    """
    Open WhatsApp Desktop and navigate to a specific chat.
    
    Args:
        contact_name: Name of the contact to open chat with
    
    Returns:
        Dictionary with result.
    
    Note:
        Requires WhatsApp Desktop or WhatsApp Beta to be installed and logged in.
    """
    try:
        # Step 1: Open Windows search (Win key)
        print("Opening Windows search...")
        pyautogui.hotkey('win')
        time.sleep(0.8)
        
        # Step 2: Type "WhatsApp" (works for both WhatsApp and WhatsApp Beta)
        print("Searching for WhatsApp...")
        pyautogui.typewrite('WhatsApp', interval=0.05)
        time.sleep(1)
        
        # Step 3: Press Enter to open first result
        print("Opening WhatsApp...")
        pyautogui.press('enter')
        time.sleep(3)  # Wait for WhatsApp to open
        
        # Step 4: Use Ctrl+F to focus search (or click search)
        print(f"Searching for contact: {contact_name}")
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.5)
        
        # Step 5: Type contact name
        # Use write with unicode support for names
        pyautogui.write(contact_name)
        time.sleep(1)
        
        # Step 6: Press Enter or Down+Enter to select first result
        pyautogui.press('down')
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(0.5)
        
        return {
            'success': True,
            'message': f'Opened WhatsApp chat with {contact_name}',
            'contact': contact_name
        }
        
    except pyautogui.FailSafeException:
        return {
            'success': False,
            'message': 'Automation aborted (mouse moved to corner). This is a safety feature.'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to open WhatsApp chat: {str(e)}',
            'error': str(e)
        }


def send_whatsapp(contact_name: str, message: str) -> Dict[str, any]:
    """
    Send a WhatsApp message to a contact.
    
    Args:
        contact_name: Name of the contact (as it appears in WhatsApp)
        message: Message to send
    
    Returns:
        Dictionary with result.
    
    Note:
        - WhatsApp Desktop must be installed and logged in
        - Contact must exist in your WhatsApp
        - Screen should not be locked during automation
    """
    try:
        # First, open the chat
        print(f"Opening chat with {contact_name}...")
        open_result = open_whatsapp_chat(contact_name)
        
        if not open_result['success']:
            return open_result
        
        # Wait for chat to be ready
        time.sleep(1)
        
        # Type the message
        print("Typing message...")
        # Use clipboard for unicode support
        import pyperclip
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        
        # Send the message
        print("Sending message...")
        pyautogui.press('enter')
        time.sleep(0.5)
        
        return {
            'success': True,
            'message': f'Message sent to {contact_name}',
            'contact': contact_name,
            'text': message[:50] + '...' if len(message) > 50 else message
        }
        
    except pyautogui.FailSafeException:
        return {
            'success': False,
            'message': 'Automation aborted (mouse moved to corner). This is a safety feature.'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to send WhatsApp message: {str(e)}',
            'error': str(e)
        }


def send_whatsapp_web(phone_number: str, message: str) -> Dict[str, any]:
    """
    Send WhatsApp message via WhatsApp Web (browser-based).
    Alternative approach that opens WhatsApp Web.
    
    Args:
        phone_number: Phone number with country code (e.g., +919876543210)
        message: Message to send
    
    Returns:
        Dictionary with result.
    """
    import webbrowser
    import urllib.parse
    
    try:
        # Clean phone number (remove spaces, dashes)
        phone = phone_number.replace(' ', '').replace('-', '').replace('+', '')
        
        # URL encode the message
        encoded_message = urllib.parse.quote(message)
        
        # WhatsApp Web URL
        url = f'https://web.whatsapp.com/send?phone={phone}&text={encoded_message}'
        
        # Open in browser
        webbrowser.open(url)
        
        return {
            'success': True,
            'message': f'Opened WhatsApp Web for {phone_number}. Click send to complete.',
            'phone': phone_number,
            'note': 'You need to click the send button manually in the browser'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to open WhatsApp Web: {str(e)}',
            'error': str(e)
        }


def check_whatsapp_installed() -> Dict[str, any]:
    """
    Check if WhatsApp Desktop is installed.
    
    Returns:
        Dictionary with installation status.
    """
    import shutil
    
    # Common WhatsApp paths on Windows
    possible_paths = [
        os.path.expandvars(r'%LOCALAPPDATA%\WhatsApp\WhatsApp.exe'),
        os.path.expandvars(r'%PROGRAMFILES%\WhatsApp\WhatsApp.exe'),
        os.path.expandvars(r'%PROGRAMFILES(X86)%\WhatsApp\WhatsApp.exe'),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return {
                'success': True,
                'installed': True,
                'path': path,
                'message': 'WhatsApp Desktop is installed'
            }
    
    # Check if command exists
    if shutil.which('whatsapp'):
        return {
            'success': True,
            'installed': True,
            'message': 'WhatsApp Desktop is available in PATH'
        }
    
    return {
        'success': True,
        'installed': False,
        'message': 'WhatsApp Desktop not found. Install from Microsoft Store or use send_whatsapp_web() instead.'
    }


def whatsapp_call(contact_name: str) -> Dict[str, any]:
    """
    Start a WhatsApp voice call with a contact.
    
    Args:
        contact_name: Name of the contact to call
    
    Returns:
        Dictionary with result.
    """
    try:
        # First, open the chat
        print(f"Opening chat with {contact_name}...")
        open_result = open_whatsapp_chat(contact_name)
        
        if not open_result['success']:
            return open_result
        
        # Wait for chat to be ready
        time.sleep(1.5)
        
        # Step 1: Click on corner/menu button first
        print("Clicking menu button...")
        pyautogui.click(1663, 94)
        time.sleep(0.8)
        
        # Step 2: Click on voice call button
        print("Starting voice call...")
        pyautogui.click(1417, 216)
        time.sleep(1)
        
        return {
            'success': True,
            'message': f'Starting voice call with {contact_name}',
            'response': f'Calling {contact_name} on WhatsApp',
            'contact': contact_name,
            'call_type': 'voice'
        }
        
    except pyautogui.FailSafeException:
        return {
            'success': False,
            'message': 'Automation aborted (mouse moved to corner)'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to start call: {str(e)}'
        }


def whatsapp_video_call(contact_name: str) -> Dict[str, any]:
    """
    Start a WhatsApp video call with a contact.
    
    Args:
        contact_name: Name of the contact to video call
    
    Returns:
        Dictionary with result.
    """
    try:
        # First, open the chat
        print(f"Opening chat with {contact_name}...")
        open_result = open_whatsapp_chat(contact_name)
        
        if not open_result['success']:
            return open_result
        
        # Wait for chat to be ready
        time.sleep(1.5)
        
        # Step 1: Click on corner/menu button first
        print("Clicking menu button...")
        pyautogui.click(1663, 94)
        time.sleep(0.8)
        
        # Step 2: Click on video call button (50px right of voice call)
        print("Starting video call...")
        pyautogui.click(1467, 216)
        time.sleep(1)
        
        return {
            'success': True,
            'message': f'Starting video call with {contact_name}',
            'response': f'Video calling {contact_name} on WhatsApp',
            'contact': contact_name,
            'call_type': 'video'
        }
        
    except pyautogui.FailSafeException:
        return {
            'success': False,
            'message': 'Automation aborted (mouse moved to corner)'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to start video call: {str(e)}'
        }
