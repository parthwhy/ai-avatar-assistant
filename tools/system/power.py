"""
Power Management Tool
Controls Windows power states: lock, sleep, shutdown, restart.
"""

import subprocess
import os
from typing import Dict, Optional


def lock_screen() -> Dict[str, any]:
    """
    Lock the Windows screen.
    
    Returns:
        Dictionary with success status and message.
    """
    try:
        import ctypes
        ctypes.windll.user32.LockWorkStation()
        return {
            'success': True,
            'message': 'Screen locked'
        }
    except Exception as e:
        # Fallback to command
        try:
            subprocess.run(
                ['rundll32.exe', 'user32.dll,LockWorkStation'],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return {
                'success': True,
                'message': 'Screen locked'
            }
        except Exception as e2:
            return {
                'success': False,
                'message': f'Failed to lock screen: {str(e2)}',
                'error': str(e2)
            }


def sleep() -> Dict[str, any]:
    """
    Put the computer to sleep.
    
    Returns:
        Dictionary with success status and message.
    """
    try:
        # Using rundll32 for sleep
        subprocess.run(
            ['rundll32.exe', 'powrprof.dll,SetSuspendState', '0', '1', '0'],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return {
            'success': True,
            'message': 'Computer going to sleep'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to sleep: {str(e)}',
            'error': str(e)
        }


def shutdown(delay_seconds: int = 0) -> Dict[str, any]:
    """
    Shutdown the computer.
    
    Args:
        delay_seconds: Delay before shutdown (0 for immediate)
    
    Returns:
        Dictionary with success status and message.
    """
    try:
        if delay_seconds > 0:
            subprocess.run(
                ['shutdown', '/s', '/t', str(delay_seconds)],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return {
                'success': True,
                'message': f'Computer will shutdown in {delay_seconds} seconds'
            }
        else:
            subprocess.run(
                ['shutdown', '/s', '/t', '0'],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return {
                'success': True,
                'message': 'Shutting down...'
            }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to shutdown: {str(e)}',
            'error': str(e)
        }


def restart(delay_seconds: int = 0) -> Dict[str, any]:
    """
    Restart the computer.
    
    Args:
        delay_seconds: Delay before restart (0 for immediate)
    
    Returns:
        Dictionary with success status and message.
    """
    try:
        if delay_seconds > 0:
            subprocess.run(
                ['shutdown', '/r', '/t', str(delay_seconds)],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return {
                'success': True,
                'message': f'Computer will restart in {delay_seconds} seconds'
            }
        else:
            subprocess.run(
                ['shutdown', '/r', '/t', '0'],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return {
                'success': True,
                'message': 'Restarting...'
            }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to restart: {str(e)}',
            'error': str(e)
        }


def schedule_shutdown(minutes: int) -> Dict[str, any]:
    """
    Schedule a shutdown after a specified number of minutes.
    
    Args:
        minutes: Number of minutes until shutdown
    
    Returns:
        Dictionary with success status and message.
    """
    if minutes <= 0:
        return {
            'success': False,
            'message': 'Minutes must be greater than 0'
        }
    
    seconds = minutes * 60
    return shutdown(delay_seconds=seconds)


def cancel_shutdown() -> Dict[str, any]:
    """
    Cancel a scheduled shutdown or restart.
    
    Returns:
        Dictionary with success status and message.
    """
    try:
        subprocess.run(
            ['shutdown', '/a'],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return {
            'success': True,
            'message': 'Scheduled shutdown/restart cancelled'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to cancel shutdown: {str(e)}. There may be no scheduled shutdown.',
            'error': str(e)
        }


def hibernate() -> Dict[str, any]:
    """
    Hibernate the computer.
    
    Returns:
        Dictionary with success status and message.
    """
    try:
        subprocess.run(
            ['shutdown', '/h'],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return {
            'success': True,
            'message': 'Hibernating...'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to hibernate: {str(e)}',
            'error': str(e)
        }


def log_off() -> Dict[str, any]:
    """
    Log off the current user.
    
    Returns:
        Dictionary with success status and message.
    """
    try:
        subprocess.run(
            ['shutdown', '/l'],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return {
            'success': True,
            'message': 'Logging off...'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to log off: {str(e)}',
            'error': str(e)
        }
