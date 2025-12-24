"""
Screen Analyzer Tool
Takes a screenshot and analyzes what's on screen using vision AI.
"""

import base64
import io
import os
import requests
from typing import Dict, Any

try:
    import pyautogui
    from PIL import Image
    SCREENSHOT_AVAILABLE = True
except ImportError:
    SCREENSHOT_AVAILABLE = False

from config.settings import settings


def take_screenshot_base64() -> str:
    """Take a screenshot and return as base64 string."""
    if not SCREENSHOT_AVAILABLE:
        return None
    
    screenshot = pyautogui.screenshot()
    
    # Resize for faster processing (max 1280px width)
    max_width = 1280
    if screenshot.width > max_width:
        ratio = max_width / screenshot.width
        new_size = (max_width, int(screenshot.height * ratio))
        screenshot = screenshot.resize(new_size, Image.LANCZOS)
    
    # Convert to base64
    buffer = io.BytesIO()
    screenshot.save(buffer, format='PNG')
    buffer.seek(0)
    
    return base64.b64encode(buffer.read()).decode('utf-8')


def analyze_screen(question: str = None) -> Dict[str, Any]:
    """
    Take a screenshot and analyze what's on screen.
    
    Args:
        question: Optional specific question about the screen
                  (e.g., "what buttons are visible?", "what app is open?")
    
    Returns:
        Dictionary with analysis result
    """
    if not SCREENSHOT_AVAILABLE:
        return {
            'success': False,
            'message': 'Screenshot not available. Install pyautogui and Pillow.'
        }
    
    # Get OpenRouter API key for vision model
    api_key = settings.openrouter_api_key
    if not api_key:
        api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        return {
            'success': False,
            'message': 'OpenRouter API key not configured. Set OPENROUTER_API_KEY in .env'
        }
    
    try:
        # Take screenshot
        print("Taking screenshot...")
        screenshot_b64 = take_screenshot_base64()
        
        if not screenshot_b64:
            return {
                'success': False,
                'message': 'Failed to take screenshot'
            }
        
        # Prepare the prompt
        if question:
            user_prompt = f"""Look at this screenshot and answer: {question}

Be specific and helpful. If you see buttons, menus, or options, list them clearly."""
        else:
            user_prompt = """Analyze this screenshot and describe:
1. What application or window is currently active?
2. What are the main elements visible (buttons, menus, text fields)?
3. What options or actions are available to the user?
4. Any important information displayed on screen?

Be concise but thorough."""

        # Call OpenRouter with vision model (using Qwen VL or similar)
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://sage-assistant.local",
            "X-Title": "SAGE AI Assistant"
        }
        
        # Use a vision-capable model
        payload = {
            "model": "qwen/qwen2.5-vl-72b-instruct",  # Qwen vision model
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{screenshot_b64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.3
        }
        
        print("Analyzing screen with AI...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        analysis = result['choices'][0]['message']['content']
        
        return {
            'success': True,
            'analysis': analysis,
            'message': 'Screen analyzed successfully',
            'response': analysis
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'message': f'API request failed: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Screen analysis failed: {str(e)}'
        }


def whats_on_screen() -> Dict[str, Any]:
    """
    Quick function to describe what's currently on screen.
    
    Returns:
        Dictionary with screen description
    """
    return analyze_screen("What is currently shown on this screen? List the main elements and any available options or buttons.")


def find_element_on_screen(element_description: str) -> Dict[str, Any]:
    """
    Find a specific element on screen.
    
    Args:
        element_description: Description of what to find (e.g., "save button", "search box")
    
    Returns:
        Dictionary with element location info
    """
    return analyze_screen(f"Find the '{element_description}' on this screen. Describe its location (top/bottom, left/right) and what it looks like.")


def get_screen_options() -> Dict[str, Any]:
    """
    Get available options/buttons on the current screen.
    
    Returns:
        Dictionary with available options
    """
    return analyze_screen("List ALL clickable buttons, menu items, and interactive elements visible on this screen. Format as a numbered list.")
