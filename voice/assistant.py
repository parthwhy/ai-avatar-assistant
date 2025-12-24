"""
Voice Assistant Pipeline
Orchestrates the voice interaction loop:
Wake Word -> Listen -> Execute -> Speak
"""

import threading
import time
from .wake_word import get_detector
from .speech_to_text import listen
from .text_to_speech import speak
from core.task_executor import get_executor

class VoiceAssistant:
    """
    Main voice interface for SAGE.
    Listens for wake word, then processes commands.
    """
    
    def __init__(self):
        self.detector = get_detector()
        self.executor = get_executor()
        self.running = False
        
    def start(self):
        """Start the voice assistant loop (blocking)."""
        print("SAGE Voice Assistant Started.")
        print("Say 'Hey Siri' (or configured wake word) to begin.")
        
        self.running = True
        
        # Start wake word detector
        # callbacks run on the detector thread
        self.detector.start_listening(callback=self._on_wake_word)
        
    def stop(self):
        """Stop the assistant."""
        self.running = False
        self.detector.stop()
        
    def _on_wake_word(self):
        """Called when wake word is detected."""
        if not self.running: return
        
        # 1. Acknowledge
        # speak("Yes?") # Verify if this is too slow. Maybe a beep sound is better?
        # For now, just print
        print(">>> LISTENING <<<")
        speak("Yes?")
        
        # 2. Listen
        command = listen()
        if not command:
            return
            
        # 3. Execute
        print(f"Executing: {command}")
        result = self.executor.execute(command)
        
        # 4. Speak Result
        self._handle_result(result)
        
    def _handle_result(self, result: dict):
        """Process execution result and speak response."""
        if result.get('response'):
            # Natural language response (from AI or simple intent)
            speak(result['response'])
        
        elif result.get('message'):
            # System message
            speak(result['message'])
            
        elif result.get('result'):
            # Raw result (e.g. calculation)
            speak(f"The result is {result['result']}")
            
        else:
            # Fallback
            if result.get('success'):
                speak("Done.")
            else:
                speak("I encountered an error.")

# Global instance
_assistant = None

def get_assistant():
    global _assistant
    if _assistant is None:
        _assistant = VoiceAssistant()
    return _assistant
