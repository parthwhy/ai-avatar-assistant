"""
Tier 8 Voice Manual Test
Run this to verify microphone and speaker setup.
"""

import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from voice.text_to_speech import speak
from voice.wake_word import get_detector
from voice.speech_to_text import listen
from voice.assistant import get_assistant

def test_tts():
    print("\n[Testing TTS] Speaking...")
    speak("Testing text to speech system. Can you hear me?")
    print("Done.")

def test_stt():
    print("\n[Testing STT] Please speak a sentence after the prompt...")
    text = listen()
    print(f"Result: '{text}'")
    if text:
        speak(f"I heard you say: {text}")

def test_wake_word():
    print("\n[Testing Wake Word]")
    print("Say 'Hey Siri' to trigger (Press Ctrl+C to force stop if it fails)")
    
    def on_wake():
        print(">>> WAKE WORD DETECTED! <<<")
        speak("I am listening.")
        get_detector().stop()
        
    get_detector().start_listening(callback=on_wake)

def test_full_assistant():
    print("\n[Testing Full Voice Assistant]")
    print("SAGE is now live. Say 'Hey Siri'...")
    print("(Press Ctrl+C to stop)")
    try:
        get_assistant().start()
    except KeyboardInterrupt:
        print("\nStopping assistant...")
        get_assistant().stop()

def main():
    while True:
        print("\n" + "="*40)
        print(" SAGE Voice Test Utility")
        print("="*40)
        print("1. Test Text-to-Speech (Speaker)")
        print("2. Test Speech-to-Text (Mic)")
        print("3. Test Wake Word ('Hey Siri')")
        print("4. Test Full Voice Assistant (Loop)")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ")
        
        if choice == '1':
            test_tts()
        elif choice == '2':
            test_stt()
        elif choice == '3':
            test_wake_word()
        elif choice == '4':
            test_full_assistant()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")
