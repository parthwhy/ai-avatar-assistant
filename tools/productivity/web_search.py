"""
Web Search Tool
Opens browser with search queries and URLs.
"""

import webbrowser
import urllib.parse
from typing import Dict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.settings import settings


# Search engine URLs
SEARCH_ENGINES = {
    'google': 'https://www.google.com/search?q=',
    'bing': 'https://www.bing.com/search?q=',
    'duckduckgo': 'https://duckduckgo.com/?q=',
    'youtube': 'https://www.youtube.com/results?search_query=',
    'github': 'https://github.com/search?q=',
    'stackoverflow': 'https://stackoverflow.com/search?q=',
}


def search_web(query: str, engine: str = 'google') -> Dict[str, any]:
    """
    Open a web search in the default browser.
    
    Args:
        query: Search query string
        engine: Search engine to use (google, bing, duckduckgo, youtube, github, stackoverflow)
    
    Returns:
        Dictionary with success status and message.
    """
    engine = engine.lower()
    
    if engine not in SEARCH_ENGINES:
        engine = 'google'
    
    try:
        # URL encode the query
        encoded_query = urllib.parse.quote_plus(query)
        search_url = SEARCH_ENGINES[engine] + encoded_query
        
        # Open in default browser
        webbrowser.open(search_url)
        
        return {
            'success': True,
            'message': f'Searching for "{query}" on {engine.capitalize()}',
            'url': search_url,
            'engine': engine
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to search: {str(e)}',
            'error': str(e)
        }


def open_url(url: str) -> Dict[str, any]:
    """
    Open a URL in the default browser.
    
    Args:
        url: URL to open (with or without http://)
    
    Returns:
        Dictionary with success status and message.
    """
    try:
        # Add https:// if no protocol specified
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        
        webbrowser.open(url)
        
        return {
            'success': True,
            'message': f'Opened {url}',
            'url': url
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to open URL: {str(e)}',
            'error': str(e)
        }


def search_and_get_answer(query: str) -> Dict[str, any]:
    """
    Search using DuckDuckGo Instant Answer API (no API key needed).
    Returns a direct answer if available, otherwise opens browser.
    
    Args:
        query: Question or search query
    
    Returns:
        Dictionary with answer or search result.
    """
    try:
        import requests
        
        # DuckDuckGo Instant Answer API
        api_url = 'https://api.duckduckgo.com/'
        params = {
            'q': query,
            'format': 'json',
            'no_html': 1,
            'skip_disambig': 1
        }
        
        response = requests.get(api_url, params=params, timeout=5)
        data = response.json()
        
        # Try to get an instant answer
        if data.get('AbstractText'):
            return {
                'success': True,
                'answer': data['AbstractText'],
                'source': data.get('AbstractSource', 'DuckDuckGo'),
                'url': data.get('AbstractURL', '')
            }
        elif data.get('Answer'):
            return {
                'success': True,
                'answer': data['Answer'],
                'source': 'DuckDuckGo',
                'url': ''
            }
        else:
            # No instant answer, just search
            return search_web(query, 'duckduckgo')
            
    except Exception as e:
        # Fallback to regular search
        return search_web(query, 'google')
