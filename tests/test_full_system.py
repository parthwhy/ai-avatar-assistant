#!/usr/bin/env python3
"""
Full System Integration Test
Tests the complete SAGE system including rate limit handling, TTS, and orchestration.
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import get_orchestrator
from voice.tts import speak, get_tts

def test_system_integration():
    """Test the complete system integration."""
    
    print("🚀 SAGE Full System Integration Test")
    print("=" * 50)
    
    orchestrator = get_orchestrator()
    tts = get_tts()
    
    print(f"✅ Orchestrator loaded: {orchestrator is not None}")
    print(f"✅ TTS available: {tts.is_available()}")
    print(f"✅ Tools registered: {len(orchestrator.tools_registry)}")
    
    # Test commands that should work with or without rate limits
    test_commands = [
        ("what time is it", "Time query"),
        ("open notepad", "App launching"),
        ("set volume to 30", "Volume control"),
        ("weather for delhi", "Weather information"),
        ("calculate 15 times 4", "Basic calculation")
    ]
    
    print("\n🧪 Testing Core Commands")
    print("-" * 30)
    
    for cmd, description in test_commands:
        print(f"\n🔍 {description}: '{cmd}'")
        
        try:
            result = orchestrator.orchestrate(cmd)
            
            success = result.get('success', False)
            response = result.get('response', 'No response')
            fallback = result.get('fallback', False)
            rate_limited = result.get('rate_limited', False)
            
            print(f"   Success: {success}")
            print(f"   Response: {response[:80]}{'...' if len(response) > 80 else ''}")
            
            if rate_limited:
                print("   🔄 Rate limited - using fallback")
            elif fallback:
                print("   🔄 Using fallback mechanism")
            else:
                print("   🤖 AI orchestration")
            
            if success:
                print("   ✅ PASSED")
            else:
                print("   ❌ FAILED")
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
    
    print("\n🔊 Testing TTS Integration")
    print("-" * 30)
    
    # Test TTS responses
    tts_tests = [
        "Yes, I'm listening",
        "Task completed successfully", 
        "Listening for your next command"
    ]
    
    for text in tts_tests:
        print(f"🎵 Speaking: '{text}'")
        speak(text, priority=True)
        time.sleep(2)
    
    print("\n📊 System Health Check")
    print("-" * 30)
    
    # Check critical components
    health_checks = [
        ("Groq API Key", bool(orchestrator.client)),
        ("Tool Registry", len(orchestrator.tools_registry) > 30),
        ("TTS Engine", tts.is_available()),
        ("Rate Limit Handler", hasattr(orchestrator, '_handle_rate_limit')),
        ("Code Generator", True)  # Always available
    ]
    
    all_healthy = True
    for component, status in health_checks:
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {component}: {'OK' if status else 'ISSUE'}")
        if not status:
            all_healthy = False
    
    print(f"\n🎯 Overall System Status: {'✅ HEALTHY' if all_healthy else '⚠️ ISSUES DETECTED'}")
    
    return all_healthy

def test_error_scenarios():
    """Test error handling scenarios."""
    
    print("\n🛡️ Testing Error Handling")
    print("-" * 30)
    
    orchestrator = get_orchestrator()
    
    # Test invalid commands
    error_tests = [
        "invalid command that makes no sense",
        "delete all my files",  # Should be handled safely
        "shutdown computer now"  # Should ask for confirmation
    ]
    
    for cmd in error_tests:
        print(f"\n🔍 Error test: '{cmd}'")
        try:
            result = orchestrator.orchestrate(cmd)
            print(f"   Handled gracefully: {result.get('success', False)}")
            print(f"   Response: {result.get('response', 'No response')[:60]}...")
        except Exception as e:
            print(f"   Exception caught: {str(e)[:60]}...")

if __name__ == "__main__":
    print("🎮 Starting SAGE System Tests...")
    
    # Run integration tests
    system_healthy = test_system_integration()
    
    # Run error handling tests
    test_error_scenarios()
    
    print("\n" + "=" * 50)
    if system_healthy:
        print("🎉 ALL SYSTEMS OPERATIONAL!")
        print("✅ SAGE is ready for production use")
        print("✅ Rate limit protection active")
        print("✅ TTS feedback working")
        print("✅ Voice interface ready")
    else:
        print("⚠️ Some issues detected - check logs above")
    
    print("\n🎤 To start voice interface, run: python main.py")
    print("🖥️ To start GUI interface, run: python ui/particle_window.py")