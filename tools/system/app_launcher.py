"""
App Launcher Tool - PyAutoGUI Version
Opens applications using Windows search bar automation.
"""

import time
import pyautogui
import pyperclip
from typing import Dict

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3


def open_app(app_name: str) -> Dict[str, any]:
    """
    Open an application using Windows search bar.
    
    Args:
        app_name: Name of the application to open (e.g., 'chrome', 'notepad', 'word')
    
    Returns:
        Dictionary with success status and message.
    """
    try:
        # Step 1: Press Windows key to open search
        print(f"Opening Windows search...")
        pyautogui.press('win')
        time.sleep(0.8)
        
        # Step 2: Type the app name
        print(f"Searching for: {app_name}")
        # Use clipboard for unicode support
        pyperclip.copy(app_name)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1.2)
        
        # Step 3: Press Enter to open first result
        print(f"Opening first result...")
        pyautogui.press('enter')
        time.sleep(0.5)
        
        return {
            'success': True,
            'message': f'Opened {app_name}',
            'app': app_name
        }
        
    except pyautogui.FailSafeException:
        return {
            'success': False,
            'message': 'Automation aborted (mouse moved to corner)'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to open {app_name}: {str(e)}',
            'error': str(e)
        }


def close_app(app_name: str) -> Dict[str, any]:
    """
    Close an application by name using taskkill.
    
    Args:
        app_name: Name of the application to close.
    
    Returns:
        Dictionary with success status and message.
    """
    import subprocess
    import psutil
    
    app_name_lower = app_name.lower().strip()
    
    # Common app process names
    process_mapping = {
        'chrome': 'chrome.exe',
        'google chrome': 'chrome.exe',
        'firefox': 'firefox.exe',
        'edge': 'msedge.exe',
        'notepad': 'notepad.exe',
        'word': 'WINWORD.EXE',
        'excel': 'EXCEL.EXE',
        'powerpoint': 'POWERPNT.EXE',
        'outlook': 'OUTLOOK.EXE',
        'vs code': 'Code.exe',
        'vscode': 'Code.exe',
        'spotify': 'Spotify.exe',
        'discord': 'Discord.exe',
        'slack': 'slack.exe',
        'whatsapp': 'WhatsApp.exe',
        'calculator': 'Calculator.exe',
        'calc': 'Calculator.exe'
    }
    
    process_name = process_mapping.get(app_name_lower, f'{app_name_lower}.exe')
    
    closed_count = 0
    
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name'].lower()
                if process_name.lower() in proc_name or app_name_lower in proc_name:
                    proc.terminate()
                    closed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if closed_count > 0:
            return {
                'success': True,
                'message': f'Closed {app_name} ({closed_count} process{"es" if closed_count > 1 else ""})',
                'closed_count': closed_count
            }
        else:
            return {
                'success': False,
                'message': f'{app_name} is not running',
                'closed_count': 0
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to close {app_name}: {str(e)}',
            'error': str(e)
        }


def type_text(text: str, press_enter: bool = False) -> Dict[str, any]:
    """
    Type text using PyAutoGUI (types into currently focused window).
    
    Args:
        text: Text to type
        press_enter: Whether to press Enter after typing
    
    Returns:
        Dictionary with success status and message.
    """
    try:
        # Use clipboard for unicode support and speed
        print(f"Typing text ({len(text)} characters)...")
        pyperclip.copy(text)
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)
        
        if press_enter:
            pyautogui.press('enter')
        
        return {
            'success': True,
            'message': f'Typed {len(text)} characters',
            'text_length': len(text)
        }
        
    except pyautogui.FailSafeException:
        return {
            'success': False,
            'message': 'Automation aborted (mouse moved to corner)'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to type text: {str(e)}',
            'error': str(e)
        }


def press_key(key: str) -> Dict[str, any]:
    """
    Press a keyboard key or combination.
    
    Args:
        key: Key to press (e.g., 'enter', 'tab', 'ctrl+s', 'ctrl+shift+n')
    
    Returns:
        Dictionary with success status and message.
    """
    try:
        # Handle key combinations
        if '+' in key:
            keys = [k.strip().lower() for k in key.split('+')]
            print(f"Pressing key combination: {keys}")
            pyautogui.hotkey(*keys)
        else:
            print(f"Pressing key: {key}")
            pyautogui.press(key.lower())
        
        time.sleep(0.2)
        
        return {
            'success': True,
            'message': f'Pressed {key}',
            'key': key
        }
        
    except pyautogui.FailSafeException:
        return {
            'success': False,
            'message': 'Automation aborted (mouse moved to corner)'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to press {key}: {str(e)}',
            'error': str(e)
        }


def focus_window(window_title: str) -> Dict[str, any]:
    """
    Focus a window by title.
    
    Args:
        window_title: Part of the window title to search for
    
    Returns:
        Dictionary with success status and message.
    """
    try:
        import pygetwindow as gw
        
        # Find windows matching the title
        windows = gw.getWindowsWithTitle(window_title)
        
        if windows:
            window = windows[0]
            window.activate()
            time.sleep(0.3)
            
            return {
                'success': True,
                'message': f'Focused window: {window.title}',
                'window_title': window.title
            }
        else:
            return {
                'success': False,
                'message': f'No window found with title containing: {window_title}'
            }
            
    except ImportError:
        # Fallback: use Alt+Tab approach
        return {
            'success': False,
            'message': 'pygetwindow not installed. Cannot focus window.'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to focus window: {str(e)}',
            'error': str(e)
        }