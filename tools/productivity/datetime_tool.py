"""
DateTime Tool
Provides current date and time information.
"""

from datetime import datetime
from typing import Dict, Any

def get_time() -> Dict[str, Any]:
    """Get the current time."""
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")
    return {
        'success': True,
        'result': time_str,
        'response': f"The time is {time_str}."
    }

def get_date() -> Dict[str, Any]:
    """Get the current date."""
    now = datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    return {
        'success': True,
        'result': date_str,
        'response': f"Today is {date_str}."
    }
