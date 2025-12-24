# Productivity tools module
from .web_search import search_web, open_url
from .calculator import calculate, evaluate_expression
from .weather import get_weather, get_weather_forecast
from .timer import set_timer, set_reminder, list_reminders, cancel_timer
from .clipboard import get_clipboard, set_clipboard, clear_clipboard, get_clipboard_history
from .file_search import search_files, find_recent_files
from .system_info import get_disk_space, get_system_info, get_battery_status
from .contacts import find_contact, smart_email_lookup, list_contacts
from .meeting_scheduler import schedule_meeting, quick_meeting

__all__ = [
    # Web
    'search_web', 'open_url',
    # Calculator
    'calculate', 'evaluate_expression',
    # Weather
    'get_weather', 'get_weather_forecast',
    # Timer
    'set_timer', 'set_reminder', 'list_reminders', 'cancel_timer',
    # Clipboard
    'get_clipboard', 'set_clipboard', 'clear_clipboard', 'get_clipboard_history',
    # File search
    'search_files', 'find_recent_files',
    # System info
    'get_disk_space', 'get_system_info', 'get_battery_status',
    # Contacts
    'find_contact', 'smart_email_lookup', 'list_contacts',
    # Meeting
    'schedule_meeting', 'quick_meeting',
]
