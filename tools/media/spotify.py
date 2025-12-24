"""
Spotify Control Tool
Control Spotify playback using PyAutoGUI automation.
"""

import time
from typing import Dict, Any

try:
    import pyautogui
    import pyperclip
    AUTOMATION_AVAILABLE = True
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
except ImportError:
    AUTOMATION_AVAILABLE = False


def play_song_on_spotify(song_name: str) -> Dict[str, Any]:
    """
    Search and play a song on Spotify.
    
    Args:
        song_name: Name of the song to play
    
    Returns:
        Dictionary with result
    """
    if not AUTOMATION_AVAILABLE:
        return {
            'success': False,
            'message': 'PyAutoGUI not available'
        }
    
    try:
        # Open Spotify via Windows search
        pyautogui.hotkey('win', 's')
        time.sleep(0.5)
        pyautogui.typewrite('spotify', interval=0.05)
        time.sleep(0.5)
        pyautogui.press('enter')
        
        # Wait for Spotify to open/focus
        time.sleep(2.5)
        
        # Press Ctrl+L to focus search bar (Spotify shortcut)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.5)
        
        # Clear any existing text and type song name
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        
        # Use clipboard for non-ASCII characters
        pyperclip.copy(song_name)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        
        # Press Enter to search
        pyautogui.press('enter')
        time.sleep(2)  # Wait for search results to load
        
        # Click on the first result
        # Position calibrated for user's screen (125% scaling)
        click_x = 568
        click_y = 478
        
        # Double-click to play the song
        pyautogui.doubleClick(click_x, click_y)
        time.sleep(0.5)
        
        return {
            'success': True,
            'message': f'Playing "{song_name}" on Spotify',
            'response': f'Now playing {song_name} on Spotify'
        }
        
    except pyautogui.FailSafeException:
        return {
            'success': False,
            'message': 'Automation aborted (mouse moved to corner)'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to play song: {str(e)}'
        }


def spotify_play_pause() -> Dict[str, Any]:
    """Toggle play/pause on Spotify."""
    if not AUTOMATION_AVAILABLE:
        return {'success': False, 'message': 'PyAutoGUI not available'}
    
    try:
        # Media play/pause key
        pyautogui.press('playpause')
        return {
            'success': True,
            'message': 'Toggled play/pause',
            'response': 'Toggled play pause on Spotify'
        }
    except Exception as e:
        return {'success': False, 'message': str(e)}


def spotify_next() -> Dict[str, Any]:
    """Skip to next track on Spotify."""
    if not AUTOMATION_AVAILABLE:
        return {'success': False, 'message': 'PyAutoGUI not available'}
    
    try:
        pyautogui.press('nexttrack')
        return {
            'success': True,
            'message': 'Skipped to next track',
            'response': 'Playing next track'
        }
    except Exception as e:
        return {'success': False, 'message': str(e)}


def spotify_previous() -> Dict[str, Any]:
    """Go to previous track on Spotify."""
    if not AUTOMATION_AVAILABLE:
        return {'success': False, 'message': 'PyAutoGUI not available'}
    
    try:
        pyautogui.press('prevtrack')
        return {
            'success': True,
            'message': 'Went to previous track',
            'response': 'Playing previous track'
        }
    except Exception as e:
        return {'success': False, 'message': str(e)}
