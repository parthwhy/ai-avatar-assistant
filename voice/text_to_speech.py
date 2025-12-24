"""
Text to Speech
Converts text to spoken audio using pyttsx3.
"""

import pyttsx3
import threading

class TextToSpeech:
    """TTS Engine wrapper."""
    
    def __init__(self):
        self.engine = None
        self._lock = threading.Lock()
        
    def _get_engine(self):
        """Lazy initialization of engine (must be on main thread usually)."""
        if not self.engine:
            try:
                self.engine = pyttsx3.init()
                # Optimize voice settings
                voices = self.engine.getProperty('voices')
                # Try to find a good female voice (Zira on Windows)
                for voice in voices:
                    if 'Zira' in voice.name:
                        self.engine.setProperty('voice', voice.id)
                        break
                
                self.engine.setProperty('rate', 170)  # Slightly faster than default
                self.engine.setProperty('volume', 1.0)
            except Exception as e:
                print(f"TTS Init Error: {e}")
        return self.engine

    def speak(self, text: str):
        """
        Speak the given text.
        Blocking call (runs runAndWait).
        """
        try:
            with self._lock:
                engine = self._get_engine()
                if engine:
                    print(f"Assistant: {text}")
                    engine.say(text)
                    engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")

# Global instance
_tts = None

def get_tts():
    global _tts
    if _tts is None:
        _tts = TextToSpeech()
    return _tts

def speak(text: str):
    """Global helper."""
    get_tts().speak(text)
