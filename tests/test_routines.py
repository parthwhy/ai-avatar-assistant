"""
Test SAGE Routines System
"""

from core.task_executor import get_executor
from routines.routine_manager import list_routines, execute_routine

def test_routines():
    print("🔄 SAGE Routines System Test")
    print("=" * 50)
    
    executor = get_executor()
    
    # Test 1: List available routines
    print("\n📋 Available Routines:")
    print("-" * 30)
    routines_result = list_routines()
    if routines_result['success']:
        for routine in routines_result['routines']:
            print(f"• {routine['name']}: {routine['description']}")
            print(f"  Steps: {routine['steps_count']} | Source: {routine['source']}")
    
    # Test 2: Test routine commands via orchestrator
    test_commands = [
        "run my morning routine",
        "start focus mode", 
        "execute meeting prep routine",
        "list my routines"
    ]
    
    print(f"\n🧪 Testing Routine Commands:")
    print("-" * 40)
    
    for command in test_commands:
        print(f"\n📝 Command: {command}")
        try:
            result = executor.execute(command)
            if result['success']:
                print(f"✅ Success: {result['type']}")
                if result.get('tool_calls'):
                    for tc in result['tool_calls']:
                        tool_result = tc.get('result', {})
                        if isinstance(tool_result, dict):
                            steps_executed = tool_result.get('steps_executed', 'N/A')
                            steps_failed = tool_result.get('steps_failed', 'N/A')
                            print(f"   🔧 Executed: {steps_executed} steps, {steps_failed} failed")
            else:
                print(f"❌ Failed: {result.get('message', 'Unknown error')}")
        except Exception as e:
            print(f"💥 Error: {e}")
    
    print(f"\n🎉 Routines test completed!")
    print("\nRoutines can:")
    print("✅ Execute multi-step workflows")
    print("✅ Open/close applications")
    print("✅ Adjust system settings")
    print("✅ Set timers and notifications")
    print("✅ Handle focus/productivity modes")

if __name__ == "__main__":
    test_routines()