"""
Test Document Creation Workflow
Tests: generate content -> open app -> type content
"""

from core.task_executor import get_executor
from tools.ai.content_generator import generate_content
from tools.system.app_launcher import open_app, type_text
import time

def test_document_workflow():
    print("📝 Testing Document Creation Workflow")
    print("=" * 50)
    
    executor = get_executor()
    
    # Test 1: Generate content
    print("\n1️⃣ Generating birthday invitation content...")
    content_result = generate_content(
        topic="birthday party invitation for my friend Sarah, party on December 25th at 7 PM at my house",
        content_type="invitation",
        style="friendly"
    )
    
    if content_result['success']:
        print(f"✅ Content generated ({len(content_result['content'])} characters)")
        print(f"Preview: {content_result['content'][:150]}...")
    else:
        print(f"❌ Failed: {content_result['message']}")
        return
    
    # Test 2: Open Word/Notepad
    print("\n2️⃣ Opening Notepad...")
    app_result = open_app("notepad")
    
    if app_result['success']:
        print(f"✅ {app_result['message']}")
    else:
        print(f"❌ Failed: {app_result['message']}")
        return
    
    # Wait for app to open
    time.sleep(2)
    
    # Test 3: Type the content
    print("\n3️⃣ Typing content into Notepad...")
    type_result = type_text(content_result['content'])
    
    if type_result['success']:
        print(f"✅ {type_result['message']}")
    else:
        print(f"❌ Failed: {type_result['message']}")
    
    print(f"\n🎉 Document workflow completed!")
    print("\n📋 Workflow Summary:")
    print("1. Generated birthday invitation content using AI")
    print("2. Opened Notepad using Windows search")
    print("3. Typed the generated content into Notepad")
    print("\n💡 You can now save the document manually (Ctrl+S)")

def test_orchestrator_document():
    """Test if orchestrator can handle document creation request."""
    print("\n" + "=" * 50)
    print("🤖 Testing Orchestrator Document Creation")
    print("=" * 50)
    
    executor = get_executor()
    
    # Test natural language document creation
    commands = [
        "create a birthday invitation for my friend",
        "generate a leave letter for my manager",
        "write a meeting notes template"
    ]
    
    for cmd in commands:
        print(f"\n📝 Command: {cmd}")
        result = executor.execute(cmd)
        
        if result['success']:
            print(f"✅ Success - Type: {result.get('type')}")
            if result.get('tool_calls'):
                for tc in result['tool_calls']:
                    print(f"   Tool: {tc['tool']}")
        else:
            print(f"❌ Failed: {result.get('message')}")

if __name__ == "__main__":
    # Run orchestrator test first (doesn't open apps)
    test_orchestrator_document()
    
    # Uncomment to run full workflow (opens Notepad and types)
    # print("\n" + "=" * 50)
    # print("Running full document workflow...")
    # test_document_workflow()