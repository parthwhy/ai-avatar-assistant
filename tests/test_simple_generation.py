#!/usr/bin/env python3
"""
Simple Code Generation Test
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import get_orchestrator

def test_single_generation():
    """Test one simple code generation."""
    
    print("🧪 Testing Single Code Generation")
    print("=" * 40)
    
    orchestrator = get_orchestrator()
    
    # Simple GUI task that should trigger generation
    cmd = "click the maximize button"
    print(f"🔍 Testing: '{cmd}'")
    
    try:
        result = orchestrator.orchestrate(cmd)
        
        print(f"\nResult:")
        print(f"  Success: {result.get('success', False)}")
        print(f"  Message: {result.get('message', 'No message')}")
        print(f"  Type: {result.get('type', 'normal')}")
        
        if result.get('type') == 'generated_automation':
            print("  ✅ Code generation worked!")
            gen_tool = result.get('generated_tool', {})
            print(f"  Tool name: {gen_tool.get('name', 'Unknown')}")
            print(f"  File path: {gen_tool.get('file_path', 'Unknown')}")
        elif result.get('requires_approval'):
            print("  ⚠️ Requires approval (safety check)")
        elif result.get('fallback'):
            print("  🔄 Used fallback")
        else:
            print("  ❓ Other result type")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_single_generation()