"""
API Key Manager with Rotation
Cycles through multiple API keys to avoid rate limits on free tier.
"""

import time
from typing import Optional
from .settings import settings


class APIKeyManager:
    """
    Manages multiple API keys with rotation to avoid rate limits.
    
    Free tier limits (Gemini):
    - 60 requests per minute
    - 1.5 million tokens per day
    
    With 3 keys, we effectively get:
    - 180 requests per minute
    - 4.5 million tokens per day
    """
    
    def __init__(self):
        self.keys = settings.gemini_keys.copy()
        self.current_index = 0
        self.request_counts = {i: 0 for i in range(len(self.keys))}
        self.last_reset = time.time()
        self.requests_per_minute_limit = 55  # Stay under 60 to be safe
    
    def get_key(self) -> Optional[str]:
        """
        Get the next available API key.
        Rotates to next key if current one is rate limited.
        
        Returns:
            API key string, or None if no keys available.
        """
        if not self.keys:
            return None
        
        # Reset counts every minute
        current_time = time.time()
        if current_time - self.last_reset >= 60:
            self.request_counts = {i: 0 for i in range(len(self.keys))}
            self.last_reset = current_time
        
        # Find a key that hasn't hit the limit
        attempts = 0
        while attempts < len(self.keys):
            if self.request_counts[self.current_index] < self.requests_per_minute_limit:
                key = self.keys[self.current_index]
                self.request_counts[self.current_index] += 1
                return key
            
            # Rotate to next key
            self.current_index = (self.current_index + 1) % len(self.keys)
            attempts += 1
        
        # All keys are rate limited, return current anyway (will be rate limited)
        return self.keys[self.current_index]
    
    def mark_rate_limited(self, key_index: Optional[int] = None):
        """
        Mark a key as rate limited, forcing rotation to next key.
        
        Args:
            key_index: Index of the rate limited key. If None, uses current.
        """
        if key_index is None:
            key_index = self.current_index
        
        # Set to max so it won't be selected
        self.request_counts[key_index] = self.requests_per_minute_limit
        
        # Rotate to next key
        self.current_index = (self.current_index + 1) % len(self.keys)
    
    def get_stats(self) -> dict:
        """
        Get usage statistics for all keys.
        
        Returns:
            Dictionary with key indices and their request counts.
        """
        return {
            'total_keys': len(self.keys),
            'current_index': self.current_index,
            'request_counts': self.request_counts.copy(),
            'seconds_until_reset': max(0, 60 - (time.time() - self.last_reset))
        }
    
    @property
    def has_keys(self) -> bool:
        """Check if any API keys are available."""
        return len(self.keys) > 0


# Global API key manager instance
api_key_manager = APIKeyManager()
