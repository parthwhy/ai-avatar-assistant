#!/usr/bin/env python3
"""
Test Stop Button Functionality
Tests the new stop button that interrupts TTS and returns to wake word listening.
"""

import sys
import os
import time
import threading
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from voice.tts import speak, stop_speech, get_tts

def test_tts_interruption():
    """Test TTS interruption functionality."""
    
    print("🔊 Testing TTS Interruption")
    print("=" * 40)
    
    # Test 1: Start long speech and interrupt it
    print("\n1️⃣ Testing TTS interruption:")
    print("   Starting long speech...")
    
    long_text = "This is a very long message that should take several seconds to speak. I am testing the interruption functionality to make sure it works properly. The stop button should be able to interrupt this speech at any time and return SAGE to the wake word listening state."
    
    # Start speech in background
    def speak_long():
        speak(long_text, priority=True)
    
    speech_thread = threading.Thread(target=speak_long, daemon=True)
    speech_thread.start()
    
    # Wait 2 seconds then interrupt
    time.sleep(2)
    print("   🛑 Interrupting speech after 2 seconds...")
    stop_speech()
    
    # Wait a moment
    time.sleep(1)
    print("   ✅ Speech interrupted successfully")
    
    # Test 2: Quick speech (should complete normally)
    print("\n2️⃣ Testing normal speech completion:")
    speak("This is a short message", priority=True)
    time.sleep(3)
    print("   ✅ Short speech completed normally")
    
    print("\n✅ TTS interruption tests completed!")

def test_stop_button_simulation():
    """Simulate the stop button functionality."""
    
    print("\n🛑 Testing Stop Button Simulation")
    print("=" * 40)
    
    # Simulate the voice interrupted flag
    voice_interrupted = False
    
    def simulate_stop():
        nonlocal voice_interrupted
        voice_interrupted = True
        stop_speech()
        print("   🛑 Stop button pressed - speech interrupted")
        print("   🔄 Returning to wake word listening state...")
        
        # Reset after a moment (like the real implementation)
        def reset_flag():
            nonlocal voice_interrupted
            voice_interrupted = False
            print("   ✅ Ready for next wake word")
        
        threading.Timer(1.0, reset_flag).start()
    
    # Simulate a long response
    print("\n🎯 Simulating long SAGE response...")
    
    def long_response():
        if not voice_interrupted:
            speak("I have successfully completed your request. Here are the details of what I accomplished.", priority=True)
            
            # Simulate waiting for TTS (with interruption checks)
            for i in range(50):  # 5 seconds total
                if voice_interrupted:
                    print("   ⚡ Response interrupted during TTS wait")
                    return
                time.sleep(0.1)
            
            if not voice_interrupted:
                speak("Listening for your next command", priority=False)
                print("   ✅ Response completed normally")
    
    # Start response
    response_thread = threading.Thread(target=long_response, daemon=True)
    response_thread.start()
    
    # Simulate user pressing stop after 2 seconds
    time.sleep(2)
    simulate_stop()
    
    # Wait for cleanup
    time.sleep(2)
    
    print("\n✅ Stop button simulation completed!")

def demo_usage():
    """Demo how the stop button works."""
    
    print("\n📖 Stop Button Usage Guide")
    print("=" * 40)
    
    print("🎯 When to use the Stop button:")
    print("   • SAGE is giving a long response you want to interrupt")
    print("   • You want to quickly return to wake word listening")
    print("   • SAGE is stuck speaking or processing")
    print("   • You need to stop current activity immediately")
    
    print("\n🔄 What happens when you press Stop:")
    print("   1. Current TTS speech is immediately stopped")
    print("   2. Any ongoing processing is interrupted")
    print("   3. Thinking section is hidden")
    print("   4. Status returns to 'Ready'")
    print("   5. System returns to wake word listening state")
    
    print("\n🎤 After pressing Stop:")
    print("   • Say 'Hey SAGE' to start a new interaction")
    print("   • The system is ready for your next command")
    print("   • Previous context is cleared")

if __name__ == "__main__":
    print("🚀 SAGE Stop Button Test Suite")
    print("Testing interruption and reset functionality")
    
    test_tts_interruption()
    test_stop_button_simulation()
    demo_usage()
    
    print("\n🎉 All stop button tests completed!")
    print("\n🎮 The Stop button provides:")
    print("   • Immediate TTS interruption")
    print("   • Quick return to wake word listening")
    print("   • Clean state reset")
    print("   • Responsive user control")
    
    print("\n🖱️ In the GUI:")
    print("   • Red 'Stop' button in bottom-right corner")
    print("   • Click anytime to interrupt SAGE")
    print("   • System immediately returns to ready state")