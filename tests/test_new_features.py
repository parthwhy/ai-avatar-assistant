"""
Test New Features
- PyAutoGUI open_app (Windows search)
- type_text function
- generate_content function
- Document creation workflow
"""

from core.task_executor import get_executor
import time

def test_new_features():
    print("🆕 Testing New Features")
    print("=" * 50)
    
    executor = get_executor()
    
    tests = [
        {
            "name": "Open App (PyAutoGUI)",
            "command": "open calculator",
            "description": "Uses Windows search to open app"
        },
        {
            "name": "Type Text",
            "command": "type hello world",
            "description": "Types text into focused window"
        },
        {
            "name": "Press Key",
            "command": "press enter",
            "description": "Presses keyboard key"
        },
        {
            "name": "Generate Content",
            "command": "create a birthday invitation",
            "description": "Generates content using AI"
        },
        {
            "name": "Generate Leave Letter",
            "command": "write a leave letter for my manager",
            "description": "Generates formal leave letter"
        },
        {
            "name": "Multi-step Workflow",
            "command": "open notepad and set volume to 30",
            "description": "Executes multiple tools in sequence"
        }
    ]
    
    for i, test in enumerate(tests, 1):
        print(f"\n{i}️⃣ {test['name']}")
        print(f"📝 Command: {test['command']}")
        print(f"💡 {test['description']}")
        print("-" * 40)
        
        try:
            result = executor.execute(test['command'])
            
            if result['success']:
                print(f"✅ Success")
                
                # Show tools used
                if result.get('tool_calls'):
                    for tc in result['tool_calls']:
                        print(f"   🔧 {tc['tool']}")
                
                # Show thinking
                if result.get('thinking'):
                    print(f"   🧠 {result['thinking'][:60]}...")
                    
            else:
                print(f"❌ Failed: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"💥 Error: {e}")
        
        time.sleep(1)
    
    print(f"\n🎉 All new features tested!")
    print("\n📋 New Features Summary:")
    print("• open_app: Uses PyAutoGUI + Windows search bar")
    print("• type_text: Types text into any focused window")
    print("• press_key: Presses keyboard keys/combinations")
    print("• generate_content: AI-powered content generation")
    print("• Document workflow: Generate → Open App → Type")

if __name__ == "__main__":
    test_new_features()