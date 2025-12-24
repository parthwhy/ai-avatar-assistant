"""
Timer and Reminder Tool
Sets timers and reminders with optional notifications.
"""

import threading
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.settings import settings


# Active timers and reminders
_active_timers: Dict[str, threading.Timer] = {}
_reminders: List[Dict] = []
_reminder_file = settings.data_dir / 'reminders.json'


def _load_reminders():
    """Load reminders from file."""
    global _reminders
    if _reminder_file.exists():
        try:
            with open(_reminder_file, 'r') as f:
                _reminders = json.load(f)
        except:
            _reminders = []


def _save_reminders():
    """Save reminders to file."""
    try:
        with open(_reminder_file, 'w') as f:
            json.dump(_reminders, f, indent=2)
    except:
        pass


def set_timer(minutes: float, name: str = None, callback: Callable = None) -> Dict[str, any]:
    """
    Set a timer that fires after specified minutes.
    
    Args:
        minutes: Minutes until timer fires
        name: Optional name for the timer
        callback: Optional function to call when timer fires
    
    Returns:
        Dictionary with timer info.
    """
    if minutes <= 0:
        return {
            'success': False,
            'message': 'Minutes must be greater than 0'
        }
    
    timer_id = name or f"timer_{int(time.time())}"
    
    # Cancel existing timer with same name
    if timer_id in _active_timers:
        _active_timers[timer_id].cancel()
    
    def timer_callback():
        # Default callback: show notification
        if callback:
            callback()
        else:
            _show_notification(f"Timer '{timer_id}' completed!", "SAGE Timer")
        
        # Remove from active timers
        if timer_id in _active_timers:
            del _active_timers[timer_id]
    
    # Create and start timer
    timer = threading.Timer(minutes * 60, timer_callback)
    timer.daemon = True
    timer.start()
    
    _active_timers[timer_id] = timer
    
    end_time = datetime.now() + timedelta(minutes=minutes)
    
    return {
        'success': True,
        'timer_id': timer_id,
        'minutes': minutes,
        'end_time': end_time.strftime('%H:%M:%S'),
        'message': f'Timer set for {minutes} minutes (ends at {end_time.strftime("%H:%M:%S")})'
    }


def cancel_timer(timer_id: str) -> Dict[str, any]:
    """
    Cancel an active timer.
    
    Args:
        timer_id: ID of the timer to cancel
    
    Returns:
        Dictionary with result.
    """
    if timer_id in _active_timers:
        _active_timers[timer_id].cancel()
        del _active_timers[timer_id]
        return {
            'success': True,
            'message': f'Timer "{timer_id}" cancelled'
        }
    else:
        return {
            'success': False,
            'message': f'Timer "{timer_id}" not found'
        }


def list_timers() -> Dict[str, any]:
    """
    List all active timers.
    
    Returns:
        Dictionary with active timer list.
    """
    return {
        'success': True,
        'timers': list(_active_timers.keys()),
        'count': len(_active_timers),
        'message': f'{len(_active_timers)} active timer(s)'
    }


def set_reminder(text: str, time_str: str = None, minutes: float = None) -> Dict[str, any]:
    """
    Set a reminder with text.
    
    Args:
        text: Reminder text
        time_str: Time string like "5:00 PM" or "17:00"
        minutes: Minutes from now (alternative to time_str)
    
    Returns:
        Dictionary with reminder info.
    """
    _load_reminders()
    
    reminder_id = f"reminder_{int(time.time())}"
    
    if minutes:
        remind_time = datetime.now() + timedelta(minutes=minutes)
    elif time_str:
        try:
            # Try to parse time
            for fmt in ['%H:%M', '%I:%M %p', '%I:%M%p', '%H:%M:%S']:
                try:
                    parsed = datetime.strptime(time_str.upper(), fmt)
                    remind_time = datetime.now().replace(
                        hour=parsed.hour,
                        minute=parsed.minute,
                        second=0,
                        microsecond=0
                    )
                    # If time is in the past, assume tomorrow
                    if remind_time < datetime.now():
                        remind_time += timedelta(days=1)
                    break
                except ValueError:
                    continue
            else:
                return {
                    'success': False,
                    'message': f'Could not parse time: {time_str}'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Invalid time format: {str(e)}'
            }
    else:
        return {
            'success': False,
            'message': 'Please provide either time_str or minutes'
        }
    
    # Calculate delay
    delay_seconds = (remind_time - datetime.now()).total_seconds()
    
    if delay_seconds <= 0:
        return {
            'success': False,
            'message': 'Reminder time must be in the future'
        }
    
    reminder = {
        'id': reminder_id,
        'text': text,
        'time': remind_time.isoformat(),
        'created': datetime.now().isoformat()
    }
    
    _reminders.append(reminder)
    _save_reminders()
    
    # Set timer for the reminder
    def reminder_callback():
        _show_notification(text, "SAGE Reminder")
        # Remove from list
        _reminders[:] = [r for r in _reminders if r['id'] != reminder_id]
        _save_reminders()
    
    timer = threading.Timer(delay_seconds, reminder_callback)
    timer.daemon = True
    timer.start()
    _active_timers[reminder_id] = timer
    
    return {
        'success': True,
        'reminder_id': reminder_id,
        'text': text,
        'time': remind_time.strftime('%Y-%m-%d %H:%M:%S'),
        'message': f'Reminder set for {remind_time.strftime("%H:%M")}: {text}'
    }


def list_reminders() -> Dict[str, any]:
    """
    List all reminders.
    
    Returns:
        Dictionary with reminder list.
    """
    _load_reminders()
    
    return {
        'success': True,
        'reminders': _reminders,
        'count': len(_reminders),
        'message': f'{len(_reminders)} reminder(s) set'
    }


def cancel_reminder(reminder_id: str) -> Dict[str, any]:
    """
    Cancel a reminder.
    
    Args:
        reminder_id: ID of the reminder to cancel
    
    Returns:
        Dictionary with result.
    """
    global _reminders
    _load_reminders()
    
    original_count = len(_reminders)
    _reminders = [r for r in _reminders if r['id'] != reminder_id]
    
    if len(_reminders) < original_count:
        _save_reminders()
        if reminder_id in _active_timers:
            _active_timers[reminder_id].cancel()
            del _active_timers[reminder_id]
        return {
            'success': True,
            'message': f'Reminder "{reminder_id}" cancelled'
        }
    else:
        return {
            'success': False,
            'message': f'Reminder "{reminder_id}" not found'
        }


def _show_notification(message: str, title: str = "SAGE"):
    """
    Show a Windows notification.
    """
    try:
        from ctypes import windll
        # Use Windows toast notification via PowerShell
        import subprocess
        ps_command = f'''
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
        $template = '<toast><visual><binding template="ToastText02"><text id="1">{title}</text><text id="2">{message}</text></binding></visual></toast>'
        $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
        $xml.LoadXml($template)
        $toast = New-Object Windows.UI.Notifications.ToastNotification $xml
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("SAGE").Show($toast)
        '''
        subprocess.run(['powershell', '-Command', ps_command], 
                      capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except:
        # Fallback: print to console
        print(f"\n🔔 {title}: {message}\n")
