"""
Speech to Text
Converts spoken audio to text using SpeechRecognition library.
Defaults to Google Web Speech API (online), but designed to be modular.
"""

import speech_recognition as sr
from .text_to_speech import speak

class SpeechToText:
    """STT Engine wrapper."""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def listen(self, timeout: int = 3, phrase_time_limit: int = 8) -> str:
        """
        Listen for a single command.
        
        Args:
            timeout: Max seconds to wait for phrase to start (default 8 seconds).
            phrase_time_limit: Max seconds for the entire phrase (default 15 seconds).
            
        Returns:
            The transcribed text, or empty string if failed.
        """
        try:
            with sr.Microphone() as source:
                print("Listening for command... (speak now)")
                # Adjust for ambient noise dynamically
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                
                # Set energy threshold for better detection
                self.recognizer.energy_threshold = 300
                self.recognizer.dynamic_energy_threshold = True
                
                try:
                    # Listen with longer timeout and phrase limit
                    audio = self.recognizer.listen(
                        source, 
                        timeout=timeout,  # Wait up to 8 seconds for speech to start
                        phrase_time_limit=phrase_time_limit  # Allow up to 15 seconds of speech
                    )
                    print("Processing audio...")
                    
                    # Transcribe
                    command = self.recognizer.recognize_google(audio).lower()
                    print(f"You said: {command}")
                    return command
                    
                except sr.WaitTimeoutError:
                    print("Timeout: No speech detected. Try speaking louder or closer to the mic.")
                    return ""
                except sr.UnknownValueError:
                    print("Could not understand audio. Please try again.")
                    return ""
                except sr.RequestError as e:
                    print(f"Speech Service Error: {e}")
                    speak("I'm having trouble connecting to speech services.")
                    return ""
                    
        except Exception as e:
            print(f"Microphone Error: {e}")
            if "PyAudio" in str(e):
                print("Hint: Check if microphone is connected and accessible.")
            return ""

# Global instance
_stt = None

def get_stt():
    global _stt
    if _stt is None:
        _stt = SpeechToText()
    return _stt

def listen(timeout: int = 3, phrase_time_limit: int = 8) -> str:
    """
    Global helper to listen for speech.
    
    Args:
        timeout: Max seconds to wait for speech to start (default 8).
        phrase_time_limit: Max seconds for the entire phrase (default 15).
    
    Returns:
        Transcribed text or empty string.
    """
    return get_stt().listen(timeout=timeout, phrase_time_limit=phrase_time_limit)
