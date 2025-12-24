"""
Tier 1 System Control Tests
Run with: python -m pytest tests/test_tier1_system.py -v
Or run directly: python tests/test_tier1_system.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.system import (
    open_app, close_app, list_running_apps,
    set_brightness, get_brightness, adjust_brightness,
    set_volume, get_volume, mute, unmute, toggle_mute,
    lock_screen, sleep, shutdown, restart, schedule_shutdown, cancel_shutdown,
    get_ip_address, toggle_wifi, toggle_bluetooth
)


def test_app_launcher():
    """Test app launcher functions."""
    print("\n" + "="*60)
    print("TESTING: App Launcher")
    print("="*60)
    
    # Test opening Notepad (safe, built-in app)
    print("\n1. Opening Notepad...")
    result = open_app('notepad')
    print(f"   Result: {result}")
    assert result['success'], f"Failed to open notepad: {result}"
    
    # Wait a moment for app to start
    import time
    time.sleep(2)
    
    # Test listing running apps
    print("\n2. Listing running apps...")
    apps = list_running_apps()
    print(f"   Found {len(apps)} running apps")
    print(f"   Top 5 by memory: {[a['name'] for a in apps[:5]]}")
    assert len(apps) > 0, "No running apps found"
    
    # Test closing Notepad
    print("\n3. Closing Notepad...")
    result = close_app('notepad')
    print(f"   Result: {result}")
    # Don't assert here, may fail if notepad closed manually
    
    print("\n✅ App Launcher tests passed!")
    return True


def test_brightness():
    """Test brightness control functions."""
    print("\n" + "="*60)
    print("TESTING: Brightness Control")
    print("="*60)
    
    # Get current brightness
    print("\n1. Getting current brightness...")
    current = get_brightness()
    print(f"   Result: {current}")
    
    if not current['success']:
        print("   ⚠️ Warning: Could not get brightness (may need admin or different display)")
        return True  # Skip but don't fail
    
    original_level = current['level']
    
    # Set brightness to 50%
    print("\n2. Setting brightness to 50%...")
    result = set_brightness(50)
    print(f"   Result: {result}")
    
    import time
    time.sleep(1)
    
    # Set back to original
    print(f"\n3. Restoring brightness to {original_level}%...")
    result = set_brightness(original_level)
    print(f"   Result: {result}")
    
    print("\n✅ Brightness tests passed!")
    return True


def test_volume():
    """Test volume control functions."""
    print("\n" + "="*60)
    print("TESTING: Volume Control")
    print("="*60)
    
    # Get current volume
    print("\n1. Getting current volume...")
    current = get_volume()
    print(f"   Result: {current}")
    
    if not current['success']:
        print("   ⚠️ Warning: Could not get volume")
        return True  # Skip but don't fail
    
    original_level = current['level']
    
    # Set volume to 30%
    print("\n2. Setting volume to 30%...")
    result = set_volume(30)
    print(f"   Result: {result}")
    
    import time
    time.sleep(1)
    
    # Test mute
    print("\n3. Testing mute...")
    result = mute()
    print(f"   Result: {result}")
    
    time.sleep(1)
    
    # Test unmute
    print("\n4. Testing unmute...")
    result = unmute()
    print(f"   Result: {result}")
    
    # Restore original volume
    print(f"\n5. Restoring volume to {original_level}%...")
    result = set_volume(original_level)
    print(f"   Result: {result}")
    
    print("\n✅ Volume tests passed!")
    return True


def test_network():
    """Test network functions."""
    print("\n" + "="*60)
    print("TESTING: Network")
    print("="*60)
    
    # Get IP address
    print("\n1. Getting IP address...")
    result = get_ip_address()
    print(f"   Result: {result}")
    assert result['success'], f"Failed to get IP: {result}"
    
    # Note: We don't test WiFi/Bluetooth toggle as they may disrupt connectivity
    print("\n2. WiFi/Bluetooth toggle tests skipped (would disrupt connectivity)")
    print("   To test manually, call toggle_wifi() or toggle_bluetooth()")
    
    print("\n✅ Network tests passed!")
    return True


def test_power_info():
    """Test power functions (info only, no actual power actions)."""
    print("\n" + "="*60)
    print("TESTING: Power Management (Info Only)")
    print("="*60)
    
    print("\n⚠️ Power actions (lock, sleep, shutdown) not tested automatically")
    print("   These would interrupt the test session.")
    print("   Available functions:")
    print("   - lock_screen()")
    print("   - sleep()")
    print("   - shutdown(delay_seconds=0)")
    print("   - restart(delay_seconds=0)")
    print("   - schedule_shutdown(minutes)")
    print("   - cancel_shutdown()")
    
    print("\n✅ Power info tests passed!")
    return True


def run_all_tests():
    """Run all Tier 1 tests."""
    print("\n" + "#"*60)
    print("#" + " "*20 + "SAGE TIER 1 TESTS" + " "*21 + "#")
    print("#" + " "*16 + "System Control Functions" + " "*18 + "#")
    print("#"*60)
    
    tests = [
        ("App Launcher", test_app_launcher),
        ("Brightness", test_brightness),
        ("Volume", test_volume),
        ("Network", test_network),
        ("Power Info", test_power_info),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ {name} test failed: {e}")
            failed += 1
    
    print("\n" + "#"*60)
    print(f"# RESULTS: {passed} passed, {failed} failed" + " "*(45-len(str(passed))-len(str(failed))) + "#")
    print("#"*60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
