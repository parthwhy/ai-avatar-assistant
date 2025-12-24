"""
Text Summarization Tool
Summarizes long text or URLs using AI.
"""

from typing import Dict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def summarize(text: str, max_length: str = "medium") -> Dict[str, any]:
    """
    Summarize a block of text.
    
    Args:
        text: Text to summarize
        max_length: "short" (1-2 sentences), "medium" (paragraph), "long" (detailed)
    
    Returns:
        Dictionary with summary.
    """
    from core.brain import get_brain
    
    brain = get_brain()
    
    length_instructions = {
        "short": "Summarize in 1-2 sentences.",
        "medium": "Summarize in a paragraph (3-5 sentences).",
        "long": "Provide a detailed summary with key points."
    }
    
    instruction = length_instructions.get(max_length, length_instructions["medium"])
    
    prompt = f"""{instruction}

Text to summarize:
{text[:10000]}  # Limit to avoid token limits
"""
    
    result = brain.ask(prompt)
    
    if result['success']:
        return {
            'success': True,
            'summary': result['response'],
            'original_length': len(text),
            'summary_length': len(result['response']),
            'message': 'Text summarized successfully'
        }
    
    return result


def summarize_url(url: str, max_length: str = "medium") -> Dict[str, any]:
    """
    Fetch a URL and summarize its content.
    
    Args:
        url: URL to fetch and summarize
        max_length: Summary length preference
    
    Returns:
        Dictionary with summary.
    """
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        return {
            'success': False,
            'message': 'beautifulsoup4 not installed. Run: pip install beautifulsoup4'
        }
    
    try:
        # Fetch the page
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML and extract text
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        text = ' '.join(text.split())
        
        if len(text) < 100:
            return {
                'success': False,
                'message': 'Could not extract meaningful text from URL'
            }
        
        # Summarize the extracted text
        result = summarize(text, max_length)
        if result['success']:
            result['url'] = url
        
        return result
        
    except requests.RequestException as e:
        return {
            'success': False,
            'message': f'Failed to fetch URL: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error: {str(e)}'
        }
