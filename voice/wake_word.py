"""
Wake Word Detection
Uses Picovoice Porcupine to detect keywords.
"""

import pvporcupine
import pyaudio
import struct
import sys
import threading
import time
from typing import Callable, Optional
from config.settings import settings

class WakeWordDetector:
    """Detects 'Hey Siri' or customized wake words."""
    
    def __init__(self):
        self.porcupine = None
        self.pa = None
        self.audio_stream = None
        self.listening = False
        self.stop_event = threading.Event()
        
    def start_listening(self, callback: Callable[[], None], keyword: str = 'hey siri'):
        """
        Start the wake word loop.
        
        Args:
            callback: Function to call when wake word is detected.
            keyword: Keyword to listen for.
        """
        if self.listening:
            return

        try:
            # Initialize Porcupine
            # Try to use provided access key, else might fail if free tier expired or invalid
            access_key = settings.picovoice_access_key
            if not access_key:
                print("Warning: No Picovoice Access Key found. Wake word disabled.")
                return

            self.porcupine = pvporcupine.create(
                access_key=access_key,
                keywords=[keyword]
            )
            
            self.pa = pyaudio.PyAudio()
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            
            self.listening = True
            self.stop_event.clear()
            
            print(f"Listening for wake word: '{keyword}'...")
            
            # Start loop in a thread
            # NOTE: For PyAudio, reading from stream is blocking.
            # We usually run this in a loop.
            
            while not self.stop_event.is_set():
                pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                
                keyword_index = self.porcupine.process(pcm)
                
                if keyword_index >= 0:
                    print("output: Wake Word Detected!")
                    if callback:
                        callback()
            
        except Exception as e:
            print(f"Wake Word Error: {e}")
        finally:
            self.cleanup()
            
    def stop(self):
        """Stop listening."""
        self.stop_event.set()
        self.listening = False

    def cleanup(self):
        """Release resources."""
        if self.audio_stream:
            self.audio_stream.close()
        if self.pa:
            self.pa.terminate()
        if self.porcupine:
            self.porcupine.delete()
        self.listening = False

# Global instance
_detector = None

def get_detector():
    global _detector
    if _detector is None:
        _detector = WakeWordDetector()
    return _detector
