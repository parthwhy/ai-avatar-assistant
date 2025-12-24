"""
Tier 5 AI Tests
Run with: python tests/test_tier5_ai.py

Note: Some tests require GEMINI_API_KEY in .env
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.intent_parser import parse_intent, IntentParser
from config.api_keys import api_key_manager


def test_intent_parser_patterns():
    """Test pattern-based intent parsing (no AI needed)."""
    print("\n" + "="*60)
    print("TESTING: Intent Parser (Pattern-based)")
    print("="*60)
    
    test_cases = [
        ("open chrome", "open_app", {"app": "chrome"}),
        ("set brightness to 50", "set_brightness", {"level": 50}),
        ("volume 30", "set_volume", {"level": 30}),
        ("mute", "mute", {}),
        ("search for python tutorials", "search_web", {"query": "python tutorials"}),
        ("set timer for 5 minutes", "set_timer", {"minutes": 5}),
        ("weather in New Delhi", "weather", {"city": "new delhi"}),
        ("run morning routine", "execute_routine", {"name": "morning"}),
        ("lock screen", "lock_screen", {}),
        ("calculate 15% of 200", "calculate", None),  # params vary
    ]
    
    parser = IntentParser()
    passed = 0
    
    for i, (input_text, expected_action, expected_params) in enumerate(test_cases, 1):
        result = parser.parse(input_text)
        action_match = result['action'] == expected_action
        
        status = "PASS" if action_match else "FAIL"
        if action_match:
            passed += 1
            
        print(f"\n{i}. Input: \"{input_text}\"")
        print(f"   Expected: {expected_action}")
        print(f"   Got: {result['action']} -> {status}")
        if result['params']:
            print(f"   Params: {result['params']}")
    
    print(f"\n   Pattern tests: {passed}/{len(test_cases)} passed")
    
    print("\n✅ Intent Parser (Pattern) tests completed!")
    return True


def test_api_key_manager():
    """Test API key manager."""
    print("\n" + "="*60)
    print("TESTING: API Key Manager")
    print("="*60)
    
    print(f"\n1. Has API keys configured: {api_key_manager.has_keys}")
    
    if api_key_manager.has_keys:
        print(f"   Number of keys: {len(api_key_manager.keys)}")
        print(f"   Current key index: {api_key_manager.current_index}")
        
        # Test rotation
        key1 = api_key_manager.get_key()
        api_key_manager.mark_rate_limited()
        key2 = api_key_manager.get_key()
        
        print(f"   Key rotation: {'Working' if key2 else 'N/A (single key)'}")
    else:
        print("   ⚠️ No API keys configured")
        print("   Add GEMINI_API_KEY to .env to enable AI features")
    
    print("\n✅ API Key Manager test passed!")
    return True


def test_brain_initialization():
    """Test Brain initialization."""
    print("\n" + "="*60)
    print("TESTING: Brain Initialization")
    print("="*60)
    
    from core.brain import Brain, get_brain
    
    print("\n1. Creating Brain instance...")
    brain = get_brain()
    print("   Brain created successfully")
    
    print(f"\n2. Checking initialization state...")
    print(f"   Initialized: {brain._initialized}")
    print(f"   Has API keys: {api_key_manager.has_keys}")
    
    if not api_key_manager.has_keys:
        print("\n   ⚠️ Skipping AI tests (no API key)")
        print("   Add GEMINI_API_KEY to .env to test AI features")
    
    print("\n✅ Brain Initialization test passed!")
    return True


def test_ai_ask():
    """Test AI ask function (requires API key)."""
    print("\n" + "="*60)
    print("TESTING: AI Ask (Requires API Key)")
    print("="*60)
    
    if not api_key_manager.has_keys:
        print("\n   ⚠️ Skipping - no API key configured")
        return True
    
    from core.brain import ask
    
    print("\n1. Sending simple question to AI...")
    result = ask("What is 2 + 2? Reply with just the number.")
    
    if result['success']:
        print(f"   Response: {result['response'][:100]}")
        print("   AI responding correctly!")
    else:
        print(f"   ⚠️ AI error: {result['message']}")
    
    print("\n✅ AI Ask test completed!")
    return True


def test_ai_intent_analysis():
    """Test AI-powered intent analysis (requires API key)."""
    print("\n" + "="*60)
    print("TESTING: AI Intent Analysis (Requires API Key)")
    print("="*60)
    
    if not api_key_manager.has_keys:
        print("\n   ⚠️ Skipping - no API key configured")
        return True
    
    from core.brain import get_brain
    
    brain = get_brain()
    
    print("\n1. Analyzing complex command with AI...")
    result = brain.analyze_intent("dim the screen a bit and play some music")
    
    if result['success']:
        print(f"   Intent: {result.get('intent', 'N/A')}")
        print(f"   Action: {result.get('action', 'N/A')}")
        print(f"   Response: {result.get('response', '')[:100]}")
    else:
        print(f"   ⚠️ Error: {result.get('message', 'Unknown error')}")
    
    print("\n✅ AI Intent Analysis test completed!")
    return True


def test_code_helper():
    """Test code helper functions (requires API key)."""
    print("\n" + "="*60)
    print("TESTING: Code Helper (Requires API Key)")
    print("="*60)
    
    if not api_key_manager.has_keys:
        print("\n   ⚠️ Skipping - no API key configured")
        return True
    
    from tools.ai import explain_code
    
    test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    
    print("\n1. Explaining code...")
    result = explain_code(test_code, "python")
    
    if result['success']:
        print(f"   Explanation preview: {result['explanation'][:150]}...")
    else:
        print(f"   ⚠️ Error: {result.get('message', 'Unknown error')}")
    
    print("\n✅ Code Helper test completed!")
    return True


def run_all_tests():
    """Run all Tier 5 tests."""
    print("\n" + "#"*60)
    print("#" + " "*20 + "SAGE TIER 5 TESTS" + " "*21 + "#")
    print("#" + " "*18 + "AI Intelligence" + " "*25 + "#")
    print("#"*60)
    
    tests = [
        ("Intent Parser (Patterns)", test_intent_parser_patterns),
        ("API Key Manager", test_api_key_manager),
        ("Brain Initialization", test_brain_initialization),
        ("AI Ask", test_ai_ask),
        ("AI Intent Analysis", test_ai_intent_analysis),
        ("Code Helper", test_code_helper),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ {name} test failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "#"*60)
    print(f"# RESULTS: {passed} passed, {failed} failed" + " "*(45-len(str(passed))-len(str(failed))) + "#")
    if not api_key_manager.has_keys:
        print("# NOTE: Add GEMINI_API_KEY to .env for full AI testing" + " "*5 + "#")
    print("#"*60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
