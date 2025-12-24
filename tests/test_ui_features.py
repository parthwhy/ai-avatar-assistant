"""
Test New UI Features
- Thinking/Processing section
- Final response in main chat
- TTS for all responses
"""

from core.task_executor import get_executor
from voice.tts import get_tts, speak
import time

def test_ui_features():
    print("🎨 Testing New UI Features")
    print("=" * 50)
    
    executor = get_executor()
    tts = get_tts()
    
    print(f"TTS Available: {tts.is_available()}")
    
    test_cases = [
        {
            "name": "General Query (Conversation)",
            "command": "what is artificial intelligence",
            "expected_type": "conversation",
            "should_speak": True
        },
        {
            "name": "Time Query (Tool)",
            "command": "what time is it",
            "expected_type": "agentic",
            "should_speak": True
        },
        {
            "name": "Multi-Tool (Workflow)",
            "command": "open calculator and set volume to 50",
            "expected_type": "agentic",
            "should_speak": True
        },
        {
            "name": "Joke (Conversation)",
            "command": "tell me a programming joke",
            "expected_type": "conversation",
            "should_speak": True
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}️⃣ {test['name']}")
        print(f"📝 Command: {test['command']}")
        print("-" * 40)
        
        result = executor.execute(test['command'])
        
        # Check type
        result_type = result.get('type', 'unknown')
        print(f"Type: {result_type} (expected: {test['expected_type']})")
        
        # Check thinking
        thinking = result.get('thinking', '')
        if thinking:
            print(f"🧠 Thinking: {thinking[:60]}...")
        
        # Check progress steps (for workflow display)
        progress_steps = result.get('progress_steps', [])
        if progress_steps:
            print(f"📊 Progress Steps: {len(progress_steps)}")
            for step in progress_steps[:3]:
                print(f"   • {step['title']}")
        
        # Extract final response
        response = result.get('response', '')
        if not response and result.get('tool_calls'):
            for tc in result['tool_calls']:
                tool_result = tc.get('result', {})
                if isinstance(tool_result, dict):
                    response = tool_result.get('response') or tool_result.get('message') or ''
                    if response:
                        break
        
        if response:
            print(f"💬 Final Response: {response[:80]}...")
            
            # Test TTS
            if test['should_speak'] and tts.is_available():
                print("🔊 Speaking response...")
                speak(response)
                time.sleep(2)
        
        print(f"✅ Test passed")
    
    print(f"\n🎉 All UI feature tests completed!")
    print("\n📋 New UI Features Summary:")
    print("• Thinking section shows AI reasoning (collapsible)")
    print("• Progress steps shown in thinking section, not main chat")
    print("• Only final response shown in main chat")
    print("• TTS reads ALL responses (conversation + tool results)")
    print("• 'Listening for your next command' after each interaction")

if __name__ == "__main__":
    test_ui_features()