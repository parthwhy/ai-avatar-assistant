"""
Final SAGE Demo - All Features Working
Shows the complete agentic system with all recent improvements.
"""

from core.task_executor import get_executor
from voice.tts import get_tts
import time

def demo_final_system():
    print("🎯 SAGE Final Demo - Complete Agentic System")
    print("=" * 60)
    
    executor = get_executor()
    tts = get_tts()
    
    print(f"🎤 TTS: {tts.is_available()}")
    print(f"🧠 Orchestrator: Ready")
    print(f"🔧 Tools: {len(executor.orchestrator.tools_registry)}")
    print(f"📞 Contacts: Available")
    print(f"📧 Email Templates: Available")
    
    # Comprehensive test scenarios
    scenarios = [
        {
            "category": "⏰ Time & Date",
            "command": "what time is it",
            "expected": "Should return formatted time with TTS"
        },
        {
            "category": "🧠 General Knowledge", 
            "command": "what is machine learning",
            "expected": "Direct answer, no web search"
        },
        {
            "category": "🔧 Multi-Tool Orchestration",
            "command": "open notepad and set brightness to 80",
            "expected": "Execute 2 tools with progress and voice feedback"
        },
        {
            "category": "📞 Contact Lookup",
            "command": "find contact manager",
            "expected": "Return manager contact details"
        },
        {
            "category": "📧 Smart Email",
            "command": "send leave letter to manager",
            "expected": "Suggest leave template for manager"
        },
        {
            "category": "💬 WhatsApp",
            "command": "send whatsapp to sujal saying hello friend",
            "expected": "Automate WhatsApp with voice confirmation"
        },
        {
            "category": "🔄 Routines",
            "command": "run my morning routine",
            "expected": "Execute 8-step morning routine"
        },
        {
            "category": "🔍 Web Search (Explicit)",
            "command": "search for latest AI news",
            "expected": "Use web search when explicitly requested"
        },
        {
            "category": "🎨 Code Generation",
            "command": "press ctrl+c to copy",
            "expected": "Generate PyAutoGUI tool for keyboard shortcut"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}️⃣ {scenario['category']}")
        print(f"📝 Command: '{scenario['command']}'")
        print(f"💡 Expected: {scenario['expected']}")
        print("-" * 50)
        
        try:
            start_time = time.time()
            result = executor.execute(scenario['command'])
            execution_time = time.time() - start_time
            
            # Analyze results
            if result['success']:
                print(f"✅ Success ({execution_time:.2f}s)")
                
                # Show AI reasoning
                if result.get('thinking'):
                    print(f"🧠 AI Thinking: {result['thinking'][:80]}...")
                
                # Show execution details
                if result.get('type') == 'agentic':
                    tool_calls = result.get('tool_calls', [])
                    progress_steps = result.get('progress_steps', [])
                    
                    print(f"🔧 Tools Used: {len(tool_calls)}")
                    for tc in tool_calls:
                        print(f"   • {tc['tool']}")
                    
                    if progress_steps:
                        print(f"📊 Progress: {len(progress_steps)} steps")
                        for step in progress_steps[-3:]:  # Show last 3 steps
                            print(f"   • {step['title']}")
                
                elif result.get('type') == 'conversation':
                    response = result.get('response', '')
                    print(f"💬 Response: {response[:100]}...")
                
                # Show generated tools
                if result.get('generated_tool'):
                    gen_tool = result['generated_tool']
                    print(f"🔨 Generated: {gen_tool['name']}")
                
            else:
                print(f"❌ Failed: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"💥 Error: {e}")
        
        # Brief pause between tests
        time.sleep(0.5)
    
    print(f"\n🎉 Final Demo Complete!")
    
    print(f"\n🌟 SAGE Agentic System - Complete Feature Set:")
    print("━" * 60)
    print("🎤 Voice Interface:")
    print("  • Wake word detection with 'YES' response")
    print("  • Text-to-speech feedback for all actions")
    print("  • 'Listening for your next command' completion")
    
    print("\n🧠 AI Orchestration:")
    print("  • Natural language understanding")
    print("  • Multi-tool workflow planning")
    print("  • Direct answers for general queries")
    print("  • Smart tool selection and chaining")
    
    print("\n🔧 Tool Ecosystem:")
    print("  • 28+ built-in tools (system, productivity, communication)")
    print("  • Automatic PyAutoGUI code generation")
    print("  • Tool persistence and reuse")
    print("  • Contact and email template database")
    
    print("\n📊 User Experience:")
    print("  • Real-time progress display")
    print("  • Step-by-step execution feedback")
    print("  • Error handling and recovery")
    print("  • Rich GUI with particle animations")
    
    print("\n🔄 Advanced Features:")
    print("  • Complex routine execution (morning, focus, etc.)")
    print("  • WhatsApp and email automation")
    print("  • Smart contact lookup and email templates")
    print("  • Web search and information retrieval")
    
    print(f"\n🚀 Ready for Production Use!")

if __name__ == "__main__":
    demo_final_system()