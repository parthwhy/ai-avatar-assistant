#!/usr/bin/env python3
"""
Quick TTS Test
Tests the text-to-speech system to ensure it's working properly.
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from voice.tts import speak, get_tts

def test_tts():
    """Test TTS functionality."""
    
    print("🔊 Testing Text-to-Speech System")
    print("=" * 40)
    
    tts = get_tts()
    
    print(f"TTS Available: {tts.is_available()}")
    print(f"TTS Enabled: {tts.enabled}")
    
    # Test short message
    print("\n🎵 Speaking: 'Hello, this is SAGE'")
    speak("Hello, this is SAGE", priority=True)
    time.sleep(3)
    
    # Test wake word response
    print("\n🎵 Speaking: 'Yes, I'm listening'")
    speak("Yes, I'm listening", priority=True)
    time.sleep(3)
    
    # Test completion message
    print("\n🎵 Speaking: 'Listening for your next command'")
    speak("Listening for your next command", priority=False)
    time.sleep(4)
    
    # Test longer message
    print("\n🎵 Speaking longer message...")
    speak("I have successfully opened Chrome browser and set the volume to 50 percent. All tasks completed successfully.", priority=True)
    time.sleep(6)
    
    print("\n✅ TTS test completed!")

if __name__ == "__main__":
    test_tts()