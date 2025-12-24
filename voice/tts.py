"""
Text-to-Speech Module
Uses Windows built-in SAPI for speech synthesis.
"""

import threading
import queue
from typing import Optional

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("Warning: pyttsx3 not installed. TTS disabled.")


class TTSEngine:
    """
    Text-to-Speech engine using pyttsx3 (Windows SAPI).
    Uses synchronous speech to avoid cutoff issues.
    """
    
    def __init__(self):
        self.enabled = True
        self.speaking = False
        self._lock = threading.Lock()
        
    def _get_engine(self):
        """Create a fresh engine instance for each speech."""
        if not TTS_AVAILABLE:
            return None
        try:
            engine = pyttsx3.init()
            
            # Configure voice settings
            voices = engine.getProperty('voices')
            if voices:
                # Try to use a female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
            
            # Set speech rate (words per minute)
            engine.setProperty('rate', 180)
            
            # Set volume (0.0 to 1.0)
            engine.setProperty('volume', 0.9)
            
            return engine
        except Exception as e:
            print(f"TTS engine creation failed: {e}")
            return None
    
    def speak(self, text: str, priority: bool = False):
        """
        Speak text synchronously in a background thread.
        
        Args:
            text: Text to speak
            priority: If True, this is a priority message
        """
        if not self.enabled or not text:
            return
        
        # Clean up text for better speech
        text = self._clean_text_for_speech(text)
        
        if not text:
            return
        
        # Run speech in background thread to not block UI
        def speak_thread():
            with self._lock:  # Ensure only one speech at a time
                self.speaking = True
                try:
                    engine = self._get_engine()
                    if engine:
                        print(f"[TTS] Speaking: {text[:60]}...")
                        engine.say(text)
                        engine.runAndWait()
                        engine.stop()
                        del engine
                except Exception as e:
                    print(f"[TTS] Error: {e}")
                finally:
                    self.speaking = False
        
        thread = threading.Thread(target=speak_thread, daemon=True)
        thread.start()
        
        # If priority, wait for it to complete
        if priority:
            thread.join(timeout=30)  # Max 30 seconds
    
    def _clean_text_for_speech(self, text: str) -> str:
        """Clean text to make it more speech-friendly."""
        # Remove common symbols that don't read well
        replacements = {
            '✅': 'Success.',
            '❌': 'Error.',
            '🔧': '',
            '📝': '',
            '💬': '',
            '🧠': '',
            '📋': '',
            '&': 'and',
            '@': 'at',
            '#': 'number',
            '%': 'percent',
            '|': '',
            '_': ' ',
            '  ': ' '  # Double spaces to single
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Limit length for speech (increased for longer responses)
        if len(text) > 500:
            text = text[:497] + "..."
        
        return text.strip()
    
    def stop(self):
        """Stop current speech and clear queue."""
        self.speaking = False
    
    def toggle(self) -> bool:
        """Toggle TTS on/off. Returns new state."""
        self.enabled = not self.enabled
        if not self.enabled:
            self.stop()
        return self.enabled
    
    def is_speaking(self) -> bool:
        """Check if currently speaking."""
        return self.speaking
    
    def is_available(self) -> bool:
        """Check if TTS is available."""
        return TTS_AVAILABLE


# Global TTS instance
_tts_engine = None

def get_tts() -> TTSEngine:
    """Get or create the global TTS engine."""
    global _tts_engine
    if _tts_engine is None:
        _tts_engine = TTSEngine()
    return _tts_engine

def speak(text: str, priority: bool = False, wait: bool = False):
    """
    Quick function to speak text.
    
    Args:
        text: Text to speak
        priority: If True, clear queue and speak immediately
        wait: If True, wait for speech to complete (blocking)
    """
    tts = get_tts()
    tts.speak(text, priority)
    
    if wait:
        # Wait for speech to complete
        import time
        while tts.is_speaking():
            time.sleep(0.1)
        time.sleep(0.5)  # Small buffer after speech

def stop_speech():
    """Quick function to stop speech."""
    get_tts().stop()

def toggle_tts() -> bool:
    """Quick function to toggle TTS."""
    return get_tts().toggle()