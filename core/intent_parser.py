"""
Intent Parser
Parses natural language commands into actionable intents.
Uses pattern matching first, falls back to AI for complex queries.
"""

import re
from typing import Dict, Optional, Tuple, List
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class IntentParser:
    """
    Parses user input into intents and parameters.
    Uses rule-based patterns for common commands, AI for complex ones.
    """
    
    def __init__(self):
        self.patterns = self._build_patterns()
    
    def _build_patterns(self) -> List[Tuple[str, str, callable]]:
        """Build regex patterns for common commands."""
        patterns = [
            # App control - capture app name, stop at common filler words
            (r'(?:open|launch|start)\s+([\w\s\+]+?)(?:\s+(?:for|please|now|app|application).*)?$', 'open_app', lambda m: {'app_name': m.group(1).strip()}),
            (r'(?:close|quit|exit|kill)\s+([\w\s\+]+?)(?:\s+(?:for|please|now|app|application).*)?$', 'close_app', lambda m: {'app_name': m.group(1).strip()}),
            
            # Brightness
            (r'(?:set\s+)?brightness\s+(?:to\s+)?(\d+)(?:\s*%)?', 'set_brightness', lambda m: {'level': int(m.group(1))}),
            (r'(?:brightness|screen)\s+(?:up|increase|higher)', 'adjust_brightness', lambda m: {'delta': 10}),
            (r'(?:brightness|screen)\s+(?:down|decrease|lower)', 'adjust_brightness', lambda m: {'delta': -10}),
            
            # Volume
            (r'(?:set\s+)?volume\s+(?:to\s+)?(\d+)(?:\s*%)?', 'set_volume', lambda m: {'level': int(m.group(1))}),
            (r'(?:volume)\s+(?:up|increase|higher)', 'adjust_volume', lambda m: {'delta': 10}),
            (r'(?:volume)\s+(?:down|decrease|lower)', 'adjust_volume', lambda m: {'delta': -10}),
            (r'\b(?:mute)\b', 'mute', lambda m: {}),
            (r'\b(?:unmute)\b', 'unmute', lambda m: {}),
            
            # Web
            (r'(?:search|google|look\s+up)\s+(?:for\s+)?(.+)', 'search_web', lambda m: {'query': m.group(1).strip()}),
            (r'(?:open|go\s+to)\s+(https?://\S+)', 'open_url', lambda m: {'url': m.group(1)}),
            (r'(?:open|go\s+to)\s+(\S+\.(?:com|org|net|io|dev|co|in))', 'open_url', lambda m: {'url': m.group(1)}),
            
            # Timer
            (r'(?:set\s+)?(?:a\s+)?timer\s+(?:for\s+)?(\d+)\s*(?:min(?:ute)?s?)?', 'set_timer', lambda m: {'minutes': int(m.group(1))}),
            (r'(?:remind\s+me|reminder)\s+(?:to\s+)?(.+?)\s+(?:in|after)\s+(\d+)\s*min', 'set_reminder', lambda m: {'text': m.group(1), 'minutes': int(m.group(2))}),
            
            # Weather
            (r'(?:what(?:\'?s|\s+is)\s+the\s+)?weather\s+(?:in\s+)?(.+)?', 'weather', lambda m: {'city': m.group(1).strip() if m.group(1) else 'current'}),
            (r'(?:how(?:\'?s|\s+is)\s+the\s+)?weather\s+(?:in\s+)?(.+)?', 'weather', lambda m: {'city': m.group(1).strip() if m.group(1) else 'current'}),
            
            # Routines
            (r'(?:start|run|execute)\s+(?:my\s+)?(?:the\s+)?(morning|focus|end\s*of\s*day|meeting\s*prep)\s*(?:routine|mode)?', 'execute_routine', 
             lambda m: {'name': m.group(1).lower().replace(' ', '_')}),
            (r'\b(morning|focus|end\s*of\s*day)\s*(?:routine|mode)\b', 'execute_routine', 
             lambda m: {'name': m.group(1).lower().replace(' ', '_')}),
            
            # Email
            (r'(?:send\s+)?email\s+(?:to\s+)?(\S+@\S+)\s+(?:about|saying)\s+(.+)', 'send_email_browser',
             lambda m: {'to': m.group(1), 'subject': m.group(2)[:50], 'body': m.group(2)}),
            
            # WhatsApp
            (r'(?:send\s+)?(?:a\s+)?whatsapp\s+(?:message\s+)?(?:to\s+)?([a-zA-Z\s]+?)(?:\s+(?:saying|message|that)\s+(.+))?$', 'send_whatsapp',
             lambda m: {'contact_name': m.group(1).strip(), 'message': m.group(2).strip() if m.group(2) else ''}),
            (r'(?:message|text|msg)\s+([a-zA-Z\s]+?)\s+(?:on\s+)?whatsapp(?:\s+(?:saying|message|that)\s+(.+))?$', 'send_whatsapp',
             lambda m: {'contact_name': m.group(1).strip(), 'message': m.group(2).strip() if m.group(2) else ''}),
            
            # System
            (r'\b(?:lock|lock\s+screen|lock\s+computer)\b', 'lock_screen', lambda m: {}),
            (r'\b(?:sleep|go\s+to\s+sleep)\b', 'sleep', lambda m: {}),
            (r'\b(?:shutdown|shut\s+down|power\s+off)\b', 'shutdown', lambda m: {}),
            (r'\b(?:restart|reboot)\b', 'restart', lambda m: {}),
            
            # Calculator
            (r'(?:what(?:\'?s|\s+is)\s+)?(\d+(?:\.\d+)?)\s*[\+\-\*\/\%]\s*(\d+(?:\.\d+)?)', 'calculate', 
             lambda m: {'expression': m.group(0)}),
            (r'(?:calculate|compute)\s+(.+)', 'calculate', lambda m: {'expression': m.group(1)}),
            (r'(?:what(?:\'?s|\s+is)\s+)?(\d+(?:\.\d+)?)\s*%\s+of\s+(\d+(?:\.\d+)?)', 'calculate',
             lambda m: {'expression': f'{m.group(1)}% of {m.group(2)}'}),
            
            # Time/Date
            (r'(?:what(?:\'?s|\s*is)\s+)?(?:the\s+)?(?:current\s+)?time', 'get_time', lambda m: {}),
            (r'(?:what(?:\'?s|\s*is)\s+)?(?:the\s+)?(?:today(?:\'?s)?\s+)?date', 'get_date', lambda m: {}),
            
            # Clipboard
            (r'(?:what(?:\'?s|\s+is)\s+)?(?:on\s+)?(?:my\s+)?clipboard', 'get_clipboard', lambda m: {}),
            
            # Disk space
            (r'(?:how\s+much\s+)?(?:disk\s+)?(?:space|storage)', 'get_disk_space', lambda m: {}),
            
            # Battery
            (r'(?:battery|battery\s+status|battery\s+level)', 'get_battery', lambda m: {}),
        ]
        
        return patterns
    
    def parse(self, user_input: str) -> Dict[str, any]:
        """
        Parse user input and extract intent.
        
        Args:
            user_input: Natural language command
        
        Returns:
            Dictionary with action and parameters.
        """
        text = user_input.lower().strip()
        
        # Try pattern matching first
        for pattern, action, param_extractor in self.patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    params = param_extractor(match)
                    return {
                        'success': True,
                        'intent': 'action',
                        'action': action,
                        'params': params,
                        'method': 'pattern',
                        'matched': match.group(0)
                    }
                except Exception as e:
                    continue
        
        # No pattern matched - could be a question or complex command
        return {
            'success': True,
            'intent': 'unknown',
            'action': None,
            'params': {},
            'method': 'none',
            'original': user_input
        }
    
    def parse_with_ai(self, user_input: str) -> Dict[str, any]:
        """
        Parse using pattern matching first, then AI fallback.
        
        Args:
            user_input: Natural language command
        
        Returns:
            Dictionary with intent and parameters.
        """
        # Try patterns first
        result = self.parse(user_input)
        
        if result['action'] is not None:
            return result
        
        # Fall back to AI
        try:
            from .brain import get_brain
            brain = get_brain()
            return brain.analyze_intent(user_input)
        except Exception as e:
            return {
                'success': False,
                'intent': 'unknown',
                'action': None,
                'params': {},
                'error': str(e)
            }


# Global parser instance
_parser = None

def get_parser() -> IntentParser:
    """Get or create the global IntentParser instance."""
    global _parser
    if _parser is None:
        _parser = IntentParser()
    return _parser


def parse_intent(user_input: str, use_ai: bool = True) -> Dict[str, any]:
    """
    Quick function to parse user intent.
    
    Args:
        user_input: Natural language command
        use_ai: Whether to use AI for unrecognized commands
    
    Returns:
        Dictionary with intent and parameters.
    """
    parser = get_parser()
    if use_ai:
        return parser.parse_with_ai(user_input)
    return parser.parse(user_input)
