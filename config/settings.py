"""
SAGE Settings Module
Loads configuration from .env file and provides app-wide settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / '.env')


class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        # Gemini API Keys (multiple for rotation)
        self.gemini_keys = self._load_gemini_keys()
        
        # Picovoice for wake word
        self.picovoice_access_key = os.getenv('PICOVOICE_ACCESS_KEY', '')
        
        # Gmail configuration
        self.gmail_address = os.getenv('GMAIL_ADDRESS', '')
        self.gmail_app_password = os.getenv('GMAIL_APP_PASSWORD', '')
        
        # User preferences
        self.default_browser = os.getenv('DEFAULT_BROWSER', 'chrome')
        self.default_brightness = int(os.getenv('DEFAULT_BRIGHTNESS', '50'))
        self.default_volume = int(os.getenv('DEFAULT_VOLUME', '50'))
        
        # Paths
        self.project_root = PROJECT_ROOT
        self.data_dir = PROJECT_ROOT / 'data'
        self.routines_dir = PROJECT_ROOT / 'routines' / 'presets'
        self.recordings_dir = PROJECT_ROOT / 'data' / 'recordings'
        self.generated_tools_dir = PROJECT_ROOT / 'data' / 'generated_tools'
        
        # Ensure data directories exist
        self._ensure_directories()
    
    def _load_gemini_keys(self) -> list:
        """Load all available Gemini API keys."""
        keys = []
        
        # Check standard single key
        single_key = os.getenv('GEMINI_API_KEY', '')
        if single_key:
            keys.append(single_key)
            
        # Check numbered keys
        for i in range(1, 10):  # Support up to 9 keys
            key = os.getenv(f'GEMINI_API_KEY_{i}', '')
            if key and key not in keys:  # Avoid duplicates
                keys.append(key)
        
        return keys
    
    def _ensure_directories(self):
        """Create necessary data directories if they don't exist."""
        self.data_dir.mkdir(exist_ok=True)
        self.recordings_dir.mkdir(parents=True, exist_ok=True)
        self.generated_tools_dir.mkdir(parents=True, exist_ok=True)
    
    @property
    def has_gemini_keys(self) -> bool:
        """Check if at least one Gemini API key is configured."""
        return len(self.gemini_keys) > 0
    
    @property
    def has_picovoice_key(self) -> bool:
        """Check if Picovoice key is configured."""
        return bool(self.picovoice_access_key)
    
    @property
    def has_gmail_config(self) -> bool:
        """Check if Gmail is configured."""
        return bool(self.gmail_address and self.gmail_app_password)

    @property
    def groq_api_key(self) -> str:
        """Load Groq API Key."""
        return os.getenv("GROQ_API_KEY", "")
    
    @property
    def openrouter_api_key(self) -> str:
        """Load OpenRouter API Key for Qwen3 Coder."""
        return os.getenv("OPENROUTER_API_KEY", "")

# Global settings instance
settings = Settings()
