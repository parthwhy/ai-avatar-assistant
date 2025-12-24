"""
Volume Control Tool
Controls system audio on Windows using pycaw.
"""

from typing import Dict
import subprocess


def _get_volume_interface():
    """Get the Windows audio interface using pycaw."""
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        return volume
    except Exception:
        return None


def set_volume(level: int) -> Dict[str, any]:
    """
    Set system volume to a specific level.
    
    Args:
        level: Volume level (0-100)
    
    Returns:
        Dictionary with success status and message.
    """
    # Clamp level to valid range
    level = max(0, min(100, level))
    
    try:
        volume = _get_volume_interface()
        if volume:
            # Convert 0-100 to 0.0-1.0
            volume.SetMasterVolumeLevelScalar(level / 100.0, None)
            return {
                'success': True,
                'message': f'Volume set to {level}%',
                'level': level
            }
        else:
            return _set_volume_nircmd(level)
    except Exception as e:
        # Try nircmd as fallback
        result = _set_volume_nircmd(level)
        if not result['success']:
            return {
                'success': False,
                'message': f'Failed to set volume: {str(e)}',
                'error': str(e)
            }
        return result


def _set_volume_nircmd(level: int) -> Dict[str, any]:
    """Set volume using PowerShell as fallback."""
    try:
        # Use PowerShell to set volume via Windows audio APIs
        # Scale 0-100 to 0-65535
        scaled = int((level / 100) * 65535)
        ps_command = f'''
        $obj = new-object -com wscript.shell
        # Mute first to reset
        1..50 | % {{ $obj.SendKeys([char]174) }}
        # Then set to desired level
        $clicks = [int]({level} / 2)
        1..$clicks | % {{ $obj.SendKeys([char]175) }}
        '''
        subprocess.run(
            ['powershell', '-Command', ps_command],
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return {
            'success': True,
            'message': f'Volume set to approximately {level}%',
            'level': level
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to set volume: {str(e)}',
            'error': str(e)
        }


def get_volume() -> Dict[str, any]:
    """
    Get current system volume level.
    
    Returns:
        Dictionary with success status and current volume level.
    """
    try:
        volume = _get_volume_interface()
        if volume:
            level = int(volume.GetMasterVolumeLevelScalar() * 100)
            return {
                'success': True,
                'level': level,
                'message': f'Current volume: {level}%'
            }
        else:
            return {
                'success': False,
                'message': 'Could not access volume interface',
                'level': None
            }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to get volume: {str(e)}',
            'error': str(e)
        }


def mute() -> Dict[str, any]:
    """
    Mute system audio.
    
    Returns:
        Dictionary with success status and message.
    """
    try:
        volume = _get_volume_interface()
        if volume:
            volume.SetMute(1, None)
            return {
                'success': True,
                'message': 'Audio muted'
            }
        else:
            return _toggle_mute_keyboard()
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to mute: {str(e)}',
            'error': str(e)
        }


def unmute() -> Dict[str, any]:
    """
    Unmute system audio.
    
    Returns:
        Dictionary with success status and message.
    """
    try:
        volume = _get_volume_interface()
        if volume:
            volume.SetMute(0, None)
            return {
                'success': True,
                'message': 'Audio unmuted'
            }
        else:
            return _toggle_mute_keyboard()
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to unmute: {str(e)}',
            'error': str(e)
        }


def toggle_mute() -> Dict[str, any]:
    """
    Toggle mute state.
    
    Returns:
        Dictionary with success status and new mute state.
    """
    try:
        volume = _get_volume_interface()
        if volume:
            current_mute = volume.GetMute()
            new_mute = 0 if current_mute else 1
            volume.SetMute(new_mute, None)
            return {
                'success': True,
                'message': 'Audio muted' if new_mute else 'Audio unmuted',
                'muted': bool(new_mute)
            }
        else:
            return _toggle_mute_keyboard()
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to toggle mute: {str(e)}',
            'error': str(e)
        }


def _toggle_mute_keyboard() -> Dict[str, any]:
    """Toggle mute using keyboard simulation."""
    try:
        import pyautogui
        # Volume mute key
        pyautogui.press('volumemute')
        return {
            'success': True,
            'message': 'Toggled mute state'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to toggle mute: {str(e)}',
            'error': str(e)
        }


def adjust_volume(delta: int) -> Dict[str, any]:
    """
    Adjust volume by a relative amount.
    
    Args:
        delta: Amount to change volume by (-100 to +100)
    
    Returns:
        Dictionary with success status and new volume level.
    """
    current = get_volume()
    if not current['success']:
        return current
    
    new_level = max(0, min(100, current['level'] + delta))
    return set_volume(new_level)
