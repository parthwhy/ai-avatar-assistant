#!/usr/bin/env python3
"""
Test Code Generator
Tests the automatic tool generation system with Qwen3 Coder.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import get_orchestrator

def test_code_generation():
    """Test code generation for a task that doesn't have an existing tool."""
    
    print("🧪 Testing Automatic Code Generation")
    print("=" * 50)
    
    orchestrator = get_orchestrator()
    
    # Test commands that should trigger code generation
    test_commands = [
        "click the maximize button in notepad",
        "right click on desktop and select refresh", 
        "press ctrl+z to undo",
        "scroll down 3 times in the current window",
        "click the close button in the top right corner"
    ]
    
    for i, cmd in enumerate(test_commands, 1):
        print(f"\n🔍 Test {i}: '{cmd}'")
        print("-" * 40)
        
        try:
            result = orchestrator.orchestrate(cmd)
            
            print(f"Success: {result.get('success', False)}")
            print(f"Type: {result.get('type', 'normal')}")
            
            if result.get('type') == 'generated_automation':
                print("✅ Code generation triggered!")
                print(f"Generated tool: {result.get('generated_tool', {}).get('name', 'Unknown')}")
                print(f"File path: {result.get('generated_tool', {}).get('file_path', 'Unknown')}")
                print(f"Reused existing: {result.get('generated_tool', {}).get('reused', False)}")
                print(f"Execution result: {result.get('execution_result', {}).get('message', 'No message')}")
            elif result.get('requires_approval'):
                print("⚠️ Generated code requires approval (safety check)")
                print(f"Reason: {result.get('message', 'No reason')}")
            elif result.get('fallback'):
                print("🔄 Used fallback mechanism")
                print(f"Response: {result.get('response', 'No response')}")
            elif result.get('rate_limited'):
                print("⏳ Rate limited - using fallback")
                print(f"Response: {result.get('response', 'No response')}")
            else:
                print("❌ Unexpected result type")
                print(f"Message: {result.get('message', 'No message')}")
                print(f"Response: {result.get('response', 'No response')}")
            
            # Show thinking if available
            if result.get('thinking'):
                print(f"AI Reasoning: {result['thinking'][:100]}...")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    print("=" * 50)
    print("🎯 Code generation test completed!")

def test_existing_tool():
    """Test a command that should use existing tools (no generation)."""
    
    print("\n🧪 Testing Existing Tool Usage")
    print("=" * 50)
    
    orchestrator = get_orchestrator()
    
    # This should use existing tools, not generate new ones
    cmd = "open chrome"
    print(f"🔍 Testing: '{cmd}'")
    
    result = orchestrator.orchestrate(cmd)
    
    print(f"Success: {result.get('success', False)}")
    print(f"Type: {result.get('type', 'normal')}")
    print(f"Fallback: {result.get('fallback', False)}")
    
    if result.get('type') == 'generated_automation':
        print("❌ Unexpected: Generated code for existing tool!")
    else:
        print("✅ Correctly used existing tool")

if __name__ == "__main__":
    print("🚀 SAGE Code Generator Test Suite")
    print("Testing automatic tool generation with Qwen3 Coder")
    
    test_code_generation()
    test_existing_tool()
    
    print("\n🎉 All tests completed!")
    print("\nℹ️  The code generator should:")
    print("   • Generate new tools for GUI automation tasks")
    print("   • Use existing tools when available")
    print("   • Apply safety checks for dangerous operations")
    print("   • Store generated tools for reuse")