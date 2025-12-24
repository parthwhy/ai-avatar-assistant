# Communication tools module
from .email_sender import send_email, validate_email, send_email_browser, quick_email, compose_email_with_content
from .whatsapp import send_whatsapp, open_whatsapp_chat, whatsapp_call, whatsapp_video_call

__all__ = [
    'send_email',
    'validate_email',
    'send_email_browser',
    'quick_email',
    'compose_email_with_content',
    'send_whatsapp',
    'open_whatsapp_chat',
    'whatsapp_call',
    'whatsapp_video_call'
]
