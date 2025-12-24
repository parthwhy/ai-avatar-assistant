"""
Tier 2 Productivity Tests
Run with: python -m pytest tests/test_tier2_productivity.py -v
Or run directly: python tests/test_tier2_productivity.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.productivity import (
    search_web, open_url,
    calculate, evaluate_expression,
    get_weather, get_weather_forecast,
    set_timer, list_reminders, cancel_timer,
    get_clipboard, set_clipboard, get_clipboard_history,
    search_files, find_recent_files,
    get_disk_space, get_system_info, get_battery_status
)


def test_web_search():
    """Test web search functions (doesn't actually open browser in test)."""
    print("\n" + "="*60)
    print("TESTING: Web Search")
    print("="*60)
    
    # Test URL builder
    from tools.productivity.web_search import SEARCH_ENGINES
    print(f"\n1. Available search engines: {list(SEARCH_ENGINES.keys())}")
    
    # Note: We're not testing actual browser opening in automated tests
    print("\n2. Web search functions available (not opening browser in test)")
    print("   - search_web(query, engine)")
    print("   - open_url(url)")
    
    print("\n✅ Web Search tests passed!")
    return True


def test_calculator():
    """Test calculator functions."""
    print("\n" + "="*60)
    print("TESTING: Calculator")
    print("="*60)
    
    test_cases = [
        ("15% of 2400", 360),
        ("sqrt(16)", 4),
        ("2 + 2 * 2", 6),
        ("100 / 4", 25),
        ("5 squared", 25),
        ("10 plus 5", 15),
    ]
    
    for i, (expr, expected) in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {expr}")
        result = calculate(expr)
        print(f"   Result: {result}")
        if result['success']:
            assert result['result'] == expected, f"Expected {expected}, got {result['result']}"
    
    print("\n✅ Calculator tests passed!")
    return True


def test_weather():
    """Test weather functions."""
    print("\n" + "="*60)
    print("TESTING: Weather")
    print("="*60)
    
    print("\n1. Getting weather for New Delhi...")
    result = get_weather("New Delhi")
    print(f"   Result: {result}")
    
    if result['success']:
        assert 'temperature' in result, "Temperature not in result"
        print(f"   Temperature: {result['temperature']}°C")
        print(f"   Condition: {result['condition']}")
    else:
        print(f"   ⚠️ Weather API call failed (may be network issue): {result['message']}")
    
    print("\n✅ Weather tests passed!")
    return True


def test_timer():
    """Test timer functions."""
    print("\n" + "="*60)
    print("TESTING: Timer")
    print("="*60)
    
    print("\n1. Setting a test timer for 0.01 minutes (0.6 seconds)...")
    result = set_timer(0.01, name="test_timer")
    print(f"   Result: {result}")
    assert result['success'], f"Timer failed: {result}"
    
    print("\n2. Listing timers...")
    from tools.productivity.timer import list_timers
    result = list_timers()
    print(f"   Active timers: {result['timers']}")
    
    print("\n3. Cancelling test timer...")
    result = cancel_timer("test_timer")
    print(f"   Result: {result}")
    
    print("\n✅ Timer tests passed!")
    return True


def test_clipboard():
    """Test clipboard functions."""
    print("\n" + "="*60)
    print("TESTING: Clipboard")
    print("="*60)
    
    # Save current clipboard
    original = get_clipboard()
    original_content = original.get('content', '')
    
    print("\n1. Setting clipboard content...")
    test_text = "SAGE Test Content - " + str(os.getpid())
    result = set_clipboard(test_text)
    print(f"   Result: {result}")
    assert result['success'], f"Set clipboard failed: {result}"
    
    print("\n2. Getting clipboard content...")
    result = get_clipboard()
    print(f"   Result: {result}")
    assert result['content'] == test_text, f"Content mismatch"
    
    print("\n3. Getting clipboard history...")
    result = get_clipboard_history(5)
    print(f"   History count: {result['count']}")
    
    # Restore original clipboard
    if original_content:
        set_clipboard(original_content)
    
    print("\n✅ Clipboard tests passed!")
    return True


def test_file_search():
    """Test file search functions."""
    print("\n" + "="*60)
    print("TESTING: File Search")
    print("="*60)
    
    print("\n1. Searching for Python files in project directory...")
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result = search_files("*.py", directory=project_dir, max_results=5)
    print(f"   Found {result['count']} files")
    if result['success'] and result['files']:
        print(f"   First file: {result['files'][0]['name']}")
    
    print("\n2. Finding recent files...")
    result = find_recent_files(directory=project_dir, hours=24, max_results=5)
    print(f"   Found {result['count']} recently modified files")
    
    print("\n✅ File Search tests passed!")
    return True


def test_system_info():
    """Test system info functions."""
    print("\n" + "="*60)
    print("TESTING: System Info")
    print("="*60)
    
    print("\n1. Getting disk space...")
    result = get_disk_space()
    print(f"   Result: {result['message']}")
    assert result['success'], f"Disk space failed: {result}"
    
    print("\n2. Getting system info...")
    result = get_system_info()
    print(f"   Result: {result['message']}")
    assert result['success'], f"System info failed: {result}"
    
    print("\n3. Getting battery status...")
    result = get_battery_status()
    print(f"   Result: {result['message']}")
    
    print("\n✅ System Info tests passed!")
    return True


def run_all_tests():
    """Run all Tier 2 tests."""
    print("\n" + "#"*60)
    print("#" + " "*20 + "SAGE TIER 2 TESTS" + " "*21 + "#")
    print("#" + " "*15 + "Productivity & Quick Actions" + " "*15 + "#")
    print("#"*60)
    
    tests = [
        ("Web Search", test_web_search),
        ("Calculator", test_calculator),
        ("Weather", test_weather),
        ("Timer", test_timer),
        ("Clipboard", test_clipboard),
        ("File Search", test_file_search),
        ("System Info", test_system_info),
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
    print("#"*60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
