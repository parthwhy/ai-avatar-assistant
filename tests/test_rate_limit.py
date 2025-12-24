#!/usr/bin/env python3
"""
Test Rate Limit Handling
Tests the fallback system when Groq API hits rate limits.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import get_orchestrator

def test_rate_limit_fallbacks():
    """Test various commands that should work with rate limit fallbacks."""
    
    orchestrator = get_orchestrator()
    
    test_commands = [
        "open chrome",
        "set volume to 50", 
        "what time is it",
        "get weather for mumbai",
        "calculate 25 plus 30",
        "open notepad",
        "volume 75"
    ]
    
    print("🧪 Testing Rate Limit Fallback System")
    print("=" * 50)
    
    for cmd in test_commands:
        print(f"\n🔍 Testing: '{cmd}'")
        
        # Force rate limit handling by calling the private method directly
        result = orchestrator._handle_rate_limit(cmd)
        
        print(f"   Success: {result.get('success', False)}")
        print(f"   Response: {result.get('response', 'No response')}")
        print(f"   Fallback: {result.get('fallback', False)}")
        
        if result.get('success'):
            print("   ✅ Fallback worked!")
        else:
            print("   ❌ Fallback failed or not applicable")
    
    print("\n" + "=" * 50)
    print("🎯 Rate limit fallback test completed!")

def test_normal_orchestration():
    """Test normal orchestration (might hit rate limit)."""
    
    orchestrator = get_orchestrator()
    
    print("\n🧪 Testing Normal Orchestration")
    print("=" * 50)
    
    # Simple command that should work
    result = orchestrator.orchestrate("what time is it")
    
    print(f"Success: {result.get('success', False)}")
    print(f"Response: {result.get('response', 'No response')}")
    print(f"Rate Limited: {result.get('rate_limited', False)}")
    print(f"Fallback: {result.get('fallback', False)}")
    
    if result.get('rate_limited'):
        print("✅ Rate limit detected and handled properly!")
    elif result.get('success'):
        print("✅ Normal orchestration worked!")
    else:
        print("❌ Something went wrong")

if __name__ == "__main__":
    print("🚀 SAGE Rate Limit Test Suite")
    print("Testing fallback mechanisms for common commands")
    
    test_rate_limit_fallbacks()
    test_normal_orchestration()
    
    print("\n🎉 All tests completed!")
    print("\nℹ️  The rate limit system provides fallbacks for:")
    print("   • App launching (chrome, notepad, etc.)")
    print("   • Volume control")
    print("   • Time queries")
    print("   • Weather information")
    print("   • Basic calculations")
    print("   • And graceful error messages for other commands")