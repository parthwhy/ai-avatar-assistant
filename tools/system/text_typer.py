"""
Text Typer Tool
Enhanced text typing functionality with various options and safety features.
"""

import time
import pyautogui
import pyperclip
from typing import Dict, Any


def type_on_screen(text: str, typing_speed: str = "normal", press_enter: bool = False) -> Dict[str, Any]:
    """
    Type text on the screen at the current cursor position.
    
    Args:
        text: Text to type on screen
        typing_speed: Speed of typing ("slow", "normal", "fast", "instant")
        press_enter: Whether to press Enter after typing
        
    Returns:
        Dictionary with operation result
    """
    try:
        if not text:
            return {
                'success': False,
                'message': 'No text provided to type'
            }
        
        # Set typing speed
        speed_settings = {
            "slow": 0.1,      # 100ms between characters
            "normal": 0.05,   # 50ms between characters  
            "fast": 0.02,     # 20ms between characters
            "instant": 0      # No delay (clipboard paste)
        }
        
        delay = speed_settings.get(typing_speed.lower(), 0.05)
        
        print(f"🖊️ Typing {len(text)} characters at {typing_speed} speed...")
        
        # For instant typing or long text, use clipboard
        if typing_speed.lower() == "instant" or len(text) > 100:
            return _type_via_clipboard(text, press_enter)
        else:
            return _type_character_by_character(text, delay, press_enter)
            
    except pyautogui.FailSafeException:
        return {
            'success': False,
            'message': 'Typing aborted (mouse moved to corner for safety)'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Typing failed: {str(e)}'
        }


def _type_via_clipboard(text: str, press_enter: bool = False) -> Dict[str, Any]:
    """Type text using clipboard paste for speed."""
    try:
        # Save current clipboard content
        original_clipboard = ""
        try:
            original_clipboard = pyperclip.paste()
        except:
            pass
        
        # Copy text to clipboard and paste
        pyperclip.copy(text)
        time.sleep(0.1)
        
        # Paste using Ctrl+V
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)
        
        # Restore original clipboard
        if original_clipboard:
            pyperclip.copy(original_clipboard)
        
        if press_enter:
            pyautogui.press('enter')
            
        return {
            'success': True,
            'message': f'Typed {len(text)} characters instantly via clipboard',
            'method': 'clipboard',
            'text_length': len(text)
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Clipboard typing failed: {str(e)}'
        }


def _type_character_by_character(text: str, delay: float, press_enter: bool = False) -> Dict[str, Any]:
    """Type text character by character with specified delay."""
    try:
        # Check if text contains special characters that pyautogui can't handle
        # pyautogui.write() only works with basic ASCII characters
        special_chars = set('!@#$%^&*()_+-=[]{}|;:\'",.<>?/`~')
        has_special = any(c in special_chars or ord(c) > 127 for c in text)
        
        if has_special:
            # Use clipboard method for text with special characters
            return _type_via_clipboard(text, press_enter)
        
        # Set PyAutoGUI typing interval
        original_pause = pyautogui.PAUSE
        pyautogui.PAUSE = delay
        
        # Type the text (only works for basic alphanumeric)
        pyautogui.write(text)
        
        # Restore original pause
        pyautogui.PAUSE = original_pause
        
        if press_enter:
            pyautogui.press('enter')
            
        return {
            'success': True,
            'message': f'Typed {len(text)} characters with {delay}s delay',
            'method': 'character_by_character',
            'text_length': len(text),
            'delay': delay
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Character typing failed: {str(e)}'
        }


def type_multiline_text(lines: list, line_delay: float = 0.5) -> Dict[str, Any]:
    """
    Type multiple lines of text with delays between lines.
    
    Args:
        lines: List of text lines to type
        line_delay: Delay between lines in seconds
        
    Returns:
        Dictionary with operation result
    """
    try:
        if not lines:
            return {
                'success': False,
                'message': 'No lines provided to type'
            }
        
        total_chars = 0
        
        for i, line in enumerate(lines):
            if line:  # Skip empty lines
                result = type_on_screen(line, typing_speed="normal", press_enter=False)
                if not result.get('success'):
                    return {
                        'success': False,
                        'message': f'Failed at line {i+1}: {result.get("message", "Unknown error")}'
                    }
                total_chars += len(line)
            
            # Press Enter and wait before next line (except for last line)
            if i < len(lines) - 1:
                pyautogui.press('enter')
                time.sleep(line_delay)
        
        return {
            'success': True,
            'message': f'Typed {len(lines)} lines ({total_chars} total characters)',
            'lines_count': len(lines),
            'total_characters': total_chars
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Multiline typing failed: {str(e)}'
        }


def type_formatted_text(text: str, format_type: str = "none") -> Dict[str, Any]:
    """
    Type text with basic formatting applied.
    
    Args:
        text: Text to type
        format_type: Type of formatting ("none", "uppercase", "lowercase", "title", "sentence")
        
    Returns:
        Dictionary with operation result
    """
    try:
        # Apply formatting
        if format_type.lower() == "uppercase":
            formatted_text = text.upper()
        elif format_type.lower() == "lowercase":
            formatted_text = text.lower()
        elif format_type.lower() == "title":
            formatted_text = text.title()
        elif format_type.lower() == "sentence":
            formatted_text = text.capitalize()
        else:
            formatted_text = text
        
        # Type the formatted text
        result = type_on_screen(formatted_text, typing_speed="normal")
        
        if result.get('success'):
            result['message'] = f'Typed {len(formatted_text)} characters with {format_type} formatting'
            result['original_length'] = len(text)
            result['formatted_length'] = len(formatted_text)
            result['formatting'] = format_type
        
        return result
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Formatted typing failed: {str(e)}'
        }


def clear_and_type(text: str, clear_method: str = "select_all") -> Dict[str, Any]:
    """
    Clear current content and type new text.
    
    Args:
        text: New text to type
        clear_method: Method to clear ("select_all", "backspace", "delete")
        
    Returns:
        Dictionary with operation result
    """
    try:
        # Clear existing content
        if clear_method.lower() == "select_all":
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
        elif clear_method.lower() == "backspace":
            # Press backspace multiple times (for short content)
            for _ in range(50):  # Clear up to 50 characters
                pyautogui.press('backspace')
                time.sleep(0.01)
        elif clear_method.lower() == "delete":
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.press('delete')
            time.sleep(0.1)
        
        # Type new text
        result = type_on_screen(text, typing_speed="instant")
        
        if result.get('success'):
            result['message'] = f'Cleared content and typed {len(text)} characters'
            result['clear_method'] = clear_method
        
        return result
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Clear and type failed: {str(e)}'
        }