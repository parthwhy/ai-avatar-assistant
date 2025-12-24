"""
Content Generator Tool
Generates various types of content using AI (documents, letters, emails, etc.)
"""

from typing import Dict, Any
from groq import Groq
from config.settings import settings


def generate_content(topic: str, content_type: str = "document", style: str = "professional") -> Dict[str, Any]:
    """
    Generate content using AI.
    
    Args:
        topic: What the content should be about
        content_type: Type of content (document, letter, email, invitation, speech, etc.)
        style: Writing style (professional, casual, formal, friendly)
    
    Returns:
        Dictionary with generated content
    """
    if not settings.groq_api_key:
        return {
            'success': False,
            'message': 'No API key available for content generation'
        }
    
    try:
        client = Groq(api_key=settings.groq_api_key)
        
        # Build prompt based on content type
        prompts = {
            'document': f"Write a {style} document about: {topic}. Include proper formatting with headings and paragraphs.",
            'letter': f"Write a {style} letter about: {topic}. Include proper letter format with greeting and closing.",
            'email': f"Write a {style} email about: {topic}. Include subject line suggestion, greeting, body, and closing.",
            'invitation': f"Write a {style} invitation for: {topic}. Make it engaging and include all necessary details.",
            'speech': f"Write a {style} speech about: {topic}. Make it engaging with a clear introduction, body, and conclusion.",
            'report': f"Write a {style} report about: {topic}. Include executive summary, main findings, and conclusion.",
            'essay': f"Write a {style} essay about: {topic}. Include introduction, body paragraphs, and conclusion.",
            'story': f"Write a creative story about: {topic}. Make it engaging with good narrative flow.",
            'poem': f"Write a poem about: {topic}. Be creative with imagery and rhythm.",
            'summary': f"Write a concise summary about: {topic}. Keep it brief but informative.",
            'list': f"Create a detailed list about: {topic}. Use bullet points or numbered items.",
            'instructions': f"Write clear instructions for: {topic}. Use step-by-step format.",
            'message': f"Write a SHORT {style} text message about: {topic}. Keep it under 100 words, casual and conversational like a WhatsApp/SMS message. Use emojis if appropriate. NO headers, NO formal structure - just a natural chat message.",
            'whatsapp': f"Write a SHORT {style} WhatsApp message about: {topic}. Keep it under 100 words, casual and conversational. Use emojis. NO headers, NO formal structure - just a natural chat message."
        }
        
        prompt = prompts.get(content_type.lower(), prompts['document'])
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": f"You are a professional content writer. Write high-quality {content_type} content. Be clear, engaging, and appropriate for the requested style."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        
        return {
            'success': True,
            'content': content,
            'content_type': content_type,
            'topic': topic,
            'style': style,
            'message': f'Generated {content_type} about {topic}'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Content generation failed: {str(e)}',
            'error': str(e)
        }


def generate_birthday_invitation(
    person_name: str,
    date: str,
    time: str,
    venue: str,
    theme: str = None,
    rsvp_contact: str = None
) -> Dict[str, Any]:
    """
    Generate a birthday invitation.
    
    Args:
        person_name: Name of the birthday person
        date: Date of the party
        time: Time of the party
        venue: Location/venue
        theme: Party theme (optional)
        rsvp_contact: RSVP contact info (optional)
    
    Returns:
        Dictionary with invitation content
    """
    details = f"""
    Birthday Person: {person_name}
    Date: {date}
    Time: {time}
    Venue: {venue}
    Theme: {theme or 'Not specified'}
    RSVP: {rsvp_contact or 'Not specified'}
    """
    
    return generate_content(
        topic=f"Birthday party invitation for {person_name}. Details: {details}",
        content_type="invitation",
        style="friendly"
    )


def generate_leave_letter(
    recipient: str,
    leave_type: str,
    start_date: str,
    end_date: str,
    reason: str,
    sender_name: str = "Employee"
) -> Dict[str, Any]:
    """
    Generate a leave application letter.
    
    Args:
        recipient: Who the letter is addressed to
        leave_type: Type of leave (sick, casual, vacation, etc.)
        start_date: Leave start date
        end_date: Leave end date
        reason: Reason for leave
        sender_name: Name of the person requesting leave
    
    Returns:
        Dictionary with letter content
    """
    details = f"""
    To: {recipient}
    Leave Type: {leave_type}
    From: {start_date}
    To: {end_date}
    Reason: {reason}
    From: {sender_name}
    """
    
    return generate_content(
        topic=f"Leave application letter. Details: {details}",
        content_type="letter",
        style="formal"
    )


def generate_meeting_notes(
    meeting_topic: str,
    attendees: str = None,
    key_points: str = None,
    action_items: str = None
) -> Dict[str, Any]:
    """
    Generate meeting notes template.
    
    Args:
        meeting_topic: Topic of the meeting
        attendees: List of attendees
        key_points: Key discussion points
        action_items: Action items from meeting
    
    Returns:
        Dictionary with meeting notes
    """
    details = f"""
    Meeting Topic: {meeting_topic}
    Attendees: {attendees or 'To be filled'}
    Key Points: {key_points or 'To be filled'}
    Action Items: {action_items or 'To be filled'}
    """
    
    return generate_content(
        topic=f"Meeting notes template. Details: {details}",
        content_type="document",
        style="professional"
    )