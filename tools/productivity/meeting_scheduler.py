"""
Meeting Scheduler Tool
Schedule Google Meet meetings, add to calendar, and send invites.
"""

import webbrowser
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import re


def parse_datetime(date_str: str, time_str: str = None) -> Optional[datetime]:
    """
    Parse date and time strings into datetime object.
    
    Supports formats like:
    - "tomorrow", "today", "next monday"
    - "15/12/2025", "2025-12-15", "December 15"
    - "6 pm", "18:00", "6:30 PM"
    """
    now = datetime.now()
    
    # Handle relative dates
    date_lower = date_str.lower().strip()
    
    if date_lower == "today":
        date_obj = now.date()
    elif date_lower == "tomorrow":
        date_obj = (now + timedelta(days=1)).date()
    elif "next" in date_lower:
        # Handle "next monday", "next week", etc.
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for i, day in enumerate(days):
            if day in date_lower:
                current_day = now.weekday()
                days_ahead = i - current_day
                if days_ahead <= 0:
                    days_ahead += 7
                date_obj = (now + timedelta(days=days_ahead)).date()
                break
        else:
            if "week" in date_lower:
                date_obj = (now + timedelta(weeks=1)).date()
            else:
                return None
    else:
        # Try parsing various date formats
        formats = [
            "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y",
            "%B %d", "%b %d", "%d %B", "%d %b",
            "%B %d, %Y", "%b %d, %Y"
        ]
        date_obj = None
        for fmt in formats:
            try:
                parsed = datetime.strptime(date_str.strip(), fmt)
                if parsed.year == 1900:  # No year provided
                    parsed = parsed.replace(year=now.year)
                date_obj = parsed.date()
                break
            except ValueError:
                continue
        
        if date_obj is None:
            return None
    
    # Parse time
    hour, minute = 10, 0  # Default to 10:00 AM
    
    if time_str:
        time_lower = time_str.lower().strip()
        
        # Handle "6 pm", "6:30 pm", "18:00"
        time_match = re.match(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', time_lower)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            
            if time_match.group(3) == 'pm' and hour < 12:
                hour += 12
            elif time_match.group(3) == 'am' and hour == 12:
                hour = 0
    
    return datetime(date_obj.year, date_obj.month, date_obj.day, hour, minute)


def schedule_meeting(
    attendee: str = None,
    title: str = None,
    date: str = None,
    time: str = None,
    duration_minutes: int = 60
) -> Dict[str, Any]:
    """
    Schedule a Google Meet meeting.
    
    Args:
        attendee: Name or email of attendee (will lookup from contacts)
        title: Meeting title/subject
        date: Date of meeting (e.g., "tomorrow", "15/12/2025")
        time: Time of meeting (e.g., "6 pm", "18:00")
        duration_minutes: Duration in minutes (default 60)
    
    Returns:
        Dictionary with meeting details or request for missing info
    """
    # Check for missing required info
    if not attendee:
        return {
            'success': False,
            'needs_info': True,
            'missing': 'attendee',
            'response': 'Who would you like to schedule the meeting with?'
        }
    
    if not date:
        return {
            'success': False,
            'needs_info': True,
            'missing': 'date',
            'response': f'When would you like to schedule the meeting with {attendee}? Please provide a date.'
        }
    
    if not time:
        return {
            'success': False,
            'needs_info': True,
            'missing': 'time',
            'response': f'What time should the meeting be on {date}?'
        }
    
    # Parse datetime
    meeting_datetime = parse_datetime(date, time)
    if not meeting_datetime:
        return {
            'success': False,
            'response': f"I couldn't understand the date/time: {date} {time}. Please try again with a format like 'tomorrow at 3 pm' or '15/12/2025 at 18:00'."
        }
    
    # Look up attendee email from contacts
    attendee_email = attendee
    attendee_name = attendee
    
    try:
        from tools.productivity.contacts import find_contact
        contact_result = find_contact(attendee)
        if contact_result['success']:
            attendee_email = contact_result['contact'].get('email', attendee)
            attendee_name = contact_result['contact'].get('name', attendee)
    except:
        pass
    
    # Generate meeting title if not provided
    if not title:
        title = f"Meeting with {attendee_name}"
    
    # Calculate end time
    end_datetime = meeting_datetime + timedelta(minutes=duration_minutes)
    
    # Format dates for Google Calendar URL
    # Format: YYYYMMDDTHHmmss
    start_str = meeting_datetime.strftime("%Y%m%dT%H%M%S")
    end_str = end_datetime.strftime("%Y%m%dT%H%M%S")
    
    # Create Google Calendar event URL with Google Meet
    # This opens Google Calendar with pre-filled event details
    calendar_params = {
        'action': 'TEMPLATE',
        'text': title,
        'dates': f'{start_str}/{end_str}',
        'details': f'Meeting scheduled via SAGE Assistant\n\nAttendee: {attendee_name} ({attendee_email})',
        'add': attendee_email,
        'crm': 'AVAILABLE',  # Add Google Meet
        'trp': 'true'  # Add conferencing
    }
    
    calendar_url = f"https://calendar.google.com/calendar/render?{urllib.parse.urlencode(calendar_params)}"
    
    # Open Google Calendar to create event
    webbrowser.open(calendar_url)
    
    # Format readable datetime
    readable_datetime = meeting_datetime.strftime("%A, %B %d, %Y at %I:%M %p")
    
    # Also prepare email with meeting details
    email_subject = f"Meeting Invitation: {title}"
    email_body = f"""Hi {attendee_name},

I'd like to schedule a meeting with you.

Meeting Details:
- Title: {title}
- Date & Time: {readable_datetime}
- Duration: {duration_minutes} minutes

A Google Meet link will be included in the calendar invite.

Please let me know if this time works for you.

Best regards"""
    
    # Open Gmail compose with meeting invite
    gmail_params = {
        'view': 'cm',
        'to': attendee_email,
        'su': email_subject,
        'body': email_body
    }
    gmail_url = f"https://mail.google.com/mail/?{urllib.parse.urlencode(gmail_params)}"
    
    # Small delay then open email
    import time
    time.sleep(1)
    webbrowser.open(gmail_url)
    
    return {
        'success': True,
        'meeting_details': {
            'title': title,
            'attendee': attendee_name,
            'attendee_email': attendee_email,
            'datetime': readable_datetime,
            'duration': duration_minutes
        },
        'message': f'Meeting scheduled with {attendee_name} on {readable_datetime}',
        'response': f"I've opened Google Calendar to create a meeting with {attendee_name} on {readable_datetime}. I've also opened Gmail with an invitation email. The Google Meet link will be automatically added to the calendar event."
    }


def quick_meeting(attendee: str) -> Dict[str, Any]:
    """
    Start a quick meeting now (opens Google Meet directly).
    
    Args:
        attendee: Person to meet with
    
    Returns:
        Dictionary with meeting link
    """
    # Open Google Meet new meeting page
    webbrowser.open("https://meet.google.com/new")
    
    return {
        'success': True,
        'message': 'Opening Google Meet',
        'response': f"I've opened Google Meet. Once the meeting starts, you can invite {attendee} by sharing the link."
    }
