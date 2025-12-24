"""
Clipboard Manager Tool
Manages clipboard with history support.
"""

import pyperclip
from typing import Dict, List
from datetime import datetime
import json
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.settings import settings


# Clipboard history
_clipboard_history: List[Dict] = []
_max_history = 50
_history_file = settings.data_dir / 'clipboard_history.json'


def _load_history():
    """Load clipboard history from file."""
    global _clipboard_history
    if _history_file.exists():
        try:
            with open(_history_file, 'r', encoding='utf-8') as f:
                _clipboard_history = json.load(f)
        except:
            _clipboard_history = []


def _save_history():
    """Save clipboard history to file."""
    try:
        with open(_history_file, 'w', encoding='utf-8') as f:
            json.dump(_clipboard_history[-_max_history:], f, indent=2, ensure_ascii=False)
    except:
        pass


def get_clipboard() -> Dict[str, any]:
    """
    Get current clipboard content.
    
    Returns:
        Dictionary with clipboard content.
    """
    try:
        content = pyperclip.paste()
        return {
            'success': True,
            'content': content,
            'length': len(content),
            'message': f'Clipboard: {content[:100]}...' if len(content) > 100 else f'Clipboard: {content}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to read clipboard: {str(e)}',
            'error': str(e)
        }


def set_clipboard(text: str) -> Dict[str, any]:
    """
    Set clipboard content and add to history.
    
    Args:
        text: Text to copy to clipboard
    
    Returns:
        Dictionary with result.
    """
    try:
        pyperclip.copy(text)
        
        # Add to history
        _load_history()
        _clipboard_history.append({
            'content': text,
            'timestamp': datetime.now().isoformat(),
            'length': len(text)
        })
        _save_history()
        
        return {
            'success': True,
            'message': f'Copied to clipboard ({len(text)} characters)',
            'length': len(text)
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to set clipboard: {str(e)}',
            'error': str(e)
        }


def clear_clipboard() -> Dict[str, any]:
    """
    Clear clipboard content.
    
    Returns:
        Dictionary with result.
    """
    try:
        pyperclip.copy('')
        return {
            'success': True,
            'message': 'Clipboard cleared'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to clear clipboard: {str(e)}',
            'error': str(e)
        }


def get_clipboard_history(count: int = 10) -> Dict[str, any]:
    """
    Get clipboard history.
    
    Args:
        count: Number of recent items to return
    
    Returns:
        Dictionary with history items.
    """
    _load_history()
    
    # Get last N items, most recent first
    recent = list(reversed(_clipboard_history[-count:]))
    
    # Truncate content for display
    display_items = []
    for item in recent:
        content = item['content']
        display_items.append({
            'preview': content[:50] + '...' if len(content) > 50 else content,
            'length': item['length'],
            'timestamp': item['timestamp']
        })
    
    return {
        'success': True,
        'history': display_items,
        'full_history': recent,
        'count': len(display_items),
        'message': f'{len(display_items)} items in clipboard history'
    }


def paste_from_history(index: int) -> Dict[str, any]:
    """
    Copy an item from history back to clipboard.
    
    Args:
        index: Index in history (0 = most recent)
    
    Returns:
        Dictionary with result.
    """
    _load_history()
    
    if not _clipboard_history:
        return {
            'success': False,
            'message': 'Clipboard history is empty'
        }
    
    # Get from end of list (most recent)
    reversed_history = list(reversed(_clipboard_history))
    
    if index < 0 or index >= len(reversed_history):
        return {
            'success': False,
            'message': f'Invalid index. History has {len(reversed_history)} items.'
        }
    
    content = reversed_history[index]['content']
    return set_clipboard(content)


def clear_history() -> Dict[str, any]:
    """
    Clear clipboard history.
    
    Returns:
        Dictionary with result.
    """
    global _clipboard_history
    _clipboard_history = []
    _save_history()
    
    return {
        'success': True,
        'message': 'Clipboard history cleared'
    }


def search_history(query: str) -> Dict[str, any]:
    """
    Search clipboard history.
    
    Args:
        query: Text to search for
    
    Returns:
        Dictionary with matching items.
    """
    _load_history()
    
    query_lower = query.lower()
    matches = [
        item for item in _clipboard_history
        if query_lower in item['content'].lower()
    ]
    
    return {
        'success': True,
        'matches': matches,
        'count': len(matches),
        'message': f'Found {len(matches)} matches for "{query}"'
    }
