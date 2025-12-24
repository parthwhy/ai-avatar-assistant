"""
Complete SAGE Agentic System Demo
Shows all features: orchestration, tool calling, code generation, progress, and TTS
"""

from core.task_executor import get_executor
from voice.tts import get_tts
import time

def demo_complete_system():
    print("🚀 SAGE Complete Agentic System Demo")
    print("=" * 60)
    
    executor = get_executor()
    tts = get_tts()
    
    print(f"🎤 TTS Available: {tts.is_available()}")
    print(f"🧠 Orchestrator: Ready")
    print(f"🔧 Tools Loaded: {len(executor.orchestrator.tools_registry)}")
    
    # Demo scenarios
    scenarios = [
        {
            "name": "Single Tool Execution",
            "command": "what time is it",
            "description": "Simple single tool call with TTS response"
        },
        {
            "name": "Multi-Tool Orchestration", 
            "command": "open calculator and set brightness to 70",
            "description": "Multiple tools executed in sequence with progress"
        },
        {
            "name": "Routine Execution",
            "command": "start my focus mode",
            "description": "Complex multi-step routine with 8 automated actions"
        },
        {
            "name": "Communication",
            "command": "send whatsapp to john saying hello there",
            "description": "WhatsApp automation with GUI interaction"
        },
        {
            "name": "Web Search",
            "command": "search for artificial intelligence news",
            "description": "Web search with browser automation"
        },
        {
            "name": "Conversation Mode",
            "command": "explain quantum computing in simple terms",
            "description": "AI conversation without tool execution"
        },
        {
            "name": "Code Generation",
            "command": "take a screenshot and save it",
            "description": "Auto-generates PyAutoGUI tool when none exists"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🎯 Scenario {i}: {scenario['name']}")
        print(f"📝 Command: {scenario['command']}")
        print(f"💡 Description: {scenario['description']}")
        print("-" * 50)
        
        try:
            start_time = time.time()
            result = executor.execute(scenario['command'])
            execution_time = time.time() - start_time
            
            # Display results
            if result['success']:
                print(f"✅ Success ({execution_time:.2f}s)")
                
                # Show thinking process
                if result.get('thinking'):
                    print(f"🧠 AI Reasoning: {result['thinking'][:80]}...")
                
                # Show progress steps
                progress_steps = result.get('progress_steps', [])
                if progress_steps:
                    print(f"📊 Progress Steps: {len(progress_steps)}")
                    for step in progress_steps:
                        print(f"   • {step['title']}")
                
                # Show tool calls
                tool_calls = result.get('tool_calls', [])
                if tool_calls:
                    print(f"🔧 Tools Used: {len(tool_calls)}")
                    for tc in tool_calls:
                        print(f"   • {tc['tool']}")
                
                # Show response
                if result.get('response'):
                    response = result['response'][:100] + "..." if len(result['response']) > 100 else result['response']
                    print(f"💬 Response: {response}")
                
                # Show generated tools
                if result.get('generated_tool'):
                    gen_tool = result['generated_tool']
                    print(f"🔨 Generated Tool: {gen_tool['name']}")
                    print(f"📁 Saved to: {gen_tool['file_path']}")
                
            else:
                print(f"❌ Failed: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"💥 Error: {e}")
        
        # Brief pause between scenarios
        time.sleep(1)
    
    print(f"\n🎉 Demo Complete!")
    print("\n🌟 SAGE Agentic System Features:")
    print("✅ Natural language understanding")
    print("✅ Multi-tool orchestration with progress tracking")
    print("✅ Text-to-speech feedback")
    print("✅ Automatic code generation for missing tools")
    print("✅ Complex routine execution")
    print("✅ GUI automation (WhatsApp, browser, etc.)")
    print("✅ Conversation mode for general queries")
    print("✅ Real-time progress display")
    print("✅ Error handling and recovery")
    print("✅ Tool persistence and reuse")

if __name__ == "__main__":
    demo_complete_system()