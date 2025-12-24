"""
SAGE Agentic System Demo
Shows the new orchestrator capabilities with tool calling and code generation.
"""

from core.task_executor import get_executor

def demo():
    print("🤖 SAGE Agentic System Demo")
    print("=" * 50)
    
    executor = get_executor()
    
    test_cases = [
        # Single tool execution
        ("Single Tool", "what time is it"),
        
        # Multi-tool execution  
        ("Multi-Tool", "open notepad and set volume to 40"),
        
        # Web search
        ("Web Search", "search for machine learning basics"),
        
        # Conversation
        ("Conversation", "explain what is artificial intelligence"),
        
        # Math
        ("Calculator", "what is 25 * 16 + 100"),
        
        # Code generation (if needed)
        ("Auto-Generation", "press the windows key"),
    ]
    
    for category, command in test_cases:
        print(f"\n📝 {category}: {command}")
        print("-" * 40)
        
        try:
            result = executor.execute(command)
            
            if result['success']:
                print(f"✅ Success: {result['type']}")
                
                if result['type'] == 'agentic':
                    print(f"🧠 Thinking: {result.get('thinking', 'N/A')}")
                    print(f"🔧 Tools: {len(result.get('tool_calls', []))}")
                    print(f"📋 Summary: {result.get('message', 'N/A')}")
                elif result['type'] == 'conversation':
                    print(f"💬 Response: {result.get('response', 'N/A')[:100]}...")
                elif result.get('type') == 'generated_automation':
                    print(f"🔨 Generated: {result.get('generated_tool', {}).get('name', 'N/A')}")
                    print(f"📁 Saved to: {result.get('generated_tool', {}).get('file_path', 'N/A')}")
            else:
                print(f"❌ Failed: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"💥 Error: {e}")
    
    print(f"\n🎉 Demo completed!")
    print("\nThe agentic system can:")
    print("✅ Execute single tools")
    print("✅ Chain multiple tools")
    print("✅ Generate new PyAutoGUI tools when needed")
    print("✅ Handle conversations")
    print("✅ Reason about user intent")

if __name__ == "__main__":
    demo()