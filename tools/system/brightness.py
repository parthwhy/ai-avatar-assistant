"""
Brightness Control Tool
Controls screen brightness on Windows.
"""

from typing import Dict, Optional
import subprocess


def set_brightness(level: int) -> Dict[str, any]:
    """
    Set screen brightness to a specific level.
    
    Args:
        level: Brightness level (0-100)
    
    Returns:
        Dictionary with success status and message.
    """
    # Clamp level to valid range
    level = max(0, min(100, level))
    
    try:
        import screen_brightness_control as sbc
        sbc.set_brightness(level)
        return {
            'success': True,
            'message': f'Brightness set to {level}%',
            'level': level
        }
    except ImportError:
        # Fallback to PowerShell
        return _set_brightness_powershell(level)
    except Exception as e:
        # Try PowerShell as fallback
        result = _set_brightness_powershell(level)
        if not result['success']:
            return {
                'success': False,
                'message': f'Failed to set brightness: {str(e)}',
                'error': str(e)
            }
        return result


def _set_brightness_powershell(level: int) -> Dict[str, any]:
    """Set brightness using PowerShell WMI."""
    try:
        ps_command = f'''
        $brightness = {level}
        $myMonitor = Get-WmiObject -Namespace root\\wmi -Class WmiMonitorBrightnessMethods
        $myMonitor.WmiSetBrightness(5, $brightness)
        '''
        subprocess.run(
            ['powershell', '-Command', ps_command],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return {
            'success': True,
            'message': f'Brightness set to {level}%',
            'level': level
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to set brightness via PowerShell: {str(e)}',
            'error': str(e)
        }


def get_brightness() -> Dict[str, any]:
    """
    Get current screen brightness level.
    
    Returns:
        Dictionary with success status and current brightness level.
    """
    try:
        import screen_brightness_control as sbc
        levels = sbc.get_brightness()
        # Returns list of brightness for each monitor, take first
        level = levels[0] if isinstance(levels, list) else levels
        return {
            'success': True,
            'level': level,
            'message': f'Current brightness: {level}%'
        }
    except ImportError:
        return _get_brightness_powershell()
    except Exception as e:
        result = _get_brightness_powershell()
        if not result['success']:
            return {
                'success': False,
                'message': f'Failed to get brightness: {str(e)}',
                'error': str(e)
            }
        return result


def _get_brightness_powershell() -> Dict[str, any]:
    """Get brightness using PowerShell WMI."""
    try:
        ps_command = '''
        (Get-WmiObject -Namespace root\\wmi -Class WmiMonitorBrightness).CurrentBrightness
        '''
        result = subprocess.run(
            ['powershell', '-Command', ps_command],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        level = int(result.stdout.strip())
        return {
            'success': True,
            'level': level,
            'message': f'Current brightness: {level}%'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to get brightness: {str(e)}',
            'error': str(e)
        }


def adjust_brightness(delta: int) -> Dict[str, any]:
    """
    Adjust brightness by a relative amount.
    
    Args:
        delta: Amount to change brightness by (-100 to +100)
    
    Returns:
        Dictionary with success status and new brightness level.
    """
    current = get_brightness()
    if not current['success']:
        return current
    
    new_level = max(0, min(100, current['level'] + delta))
    return set_brightness(new_level)
