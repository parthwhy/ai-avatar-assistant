"""
Test Progress and TTS Features
"""

from core.orchestrator import get_orchestrator
from voice.tts import get_tts

def test_progress_and_tts():
    print("🎯 Testing Progress Display and TTS")
    print("=" * 50)
    
    # Test TTS
    tts = get_tts()
    print(f"TTS Available: {tts.is_available()}")
    
    if tts.is_available():
        print("Testing TTS...")
        tts.speak("Hello, this is SAGE testing text to speech")
        import time
        time.sleep(2)
    
    # Test orchestrator with progress
    orchestrator = get_orchestrator()
    
    test_commands = [
        "open chrome and set volume to 50",
        "run my morning routine",
        "tell me a joke"
    ]
    
    for command in test_commands:
        print(f"\n📝 Command: {command}")
        print("-" * 40)
        
        result = orchestrator.orchestrate(command)
        
        print(f"Success: {result['success']}")
        print(f"Thinking: {result.get('thinking', 'N/A')}")
        
        progress_steps = result.get('progress_steps', [])
        print(f"Progress Steps: {len(progress_steps)}")
        
        for i, step in enumerate(progress_steps):
            print(f"  {i+1}. {step['title']}")
            if step.get('description'):
                print(f"     {step['description']}")
        
        if result.get('response'):
            print(f"Response: {result['response']}")
        
        print()

if __name__ == "__main__":
    test_progress_and_tts()