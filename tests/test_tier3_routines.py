"""
Tier 3 Routines Tests
Run with: python -m pytest tests/test_tier3_routines.py -v
Or run directly: python tests/test_tier3_routines.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routines import (
    create_routine,
    get_routine,
    update_routine,
    delete_routine,
    list_routines,
    execute_routine,
    add_step_to_routine,
    remove_step_from_routine
)


def test_create_routine():
    """Test creating a routine."""
    print("\n" + "="*60)
    print("TESTING: Create Routine")
    print("="*60)
    
    print("\n1. Creating test routine...")
    result = create_routine(
        name="test_routine",
        steps=[
            {"action": "wait", "params": {"seconds": 0.1}},
            {"action": "notify", "params": {"message": "Test step 1"}},
        ],
        description="A test routine"
    )
    print(f"   Result: {result['message']}")
    assert result['success'], f"Create failed: {result}"
    
    print("\n✅ Create Routine test passed!")
    return True


def test_get_routine():
    """Test getting a routine."""
    print("\n" + "="*60)
    print("TESTING: Get Routine")
    print("="*60)
    
    print("\n1. Getting test routine (custom)...")
    result = get_routine("test_routine")
    print(f"   Result: Source={result.get('source', 'N/A')}, Steps={len(result.get('routine', {}).get('steps', []))}")
    assert result['success'], f"Get failed: {result}"
    
    print("\n2. Getting morning routine (preset)...")
    result = get_routine("morning")
    print(f"   Result: Source={result.get('source', 'N/A')}, Steps={len(result.get('routine', {}).get('steps', []))}")
    assert result['success'], f"Get preset failed: {result}"
    
    print("\n✅ Get Routine test passed!")
    return True


def test_list_routines():
    """Test listing routines."""
    print("\n" + "="*60)
    print("TESTING: List Routines")
    print("="*60)
    
    print("\n1. Listing all routines...")
    result = list_routines()
    print(f"   Found {result['count']} routines:")
    for r in result['routines']:
        print(f"   - {r['name']} ({r['source']}): {r['steps_count']} steps")
    assert result['success'], f"List failed: {result}"
    
    print("\n✅ List Routines test passed!")
    return True


def test_update_routine():
    """Test updating a routine."""
    print("\n" + "="*60)
    print("TESTING: Update Routine")
    print("="*60)
    
    print("\n1. Updating test routine description...")
    result = update_routine("test_routine", description="Updated test routine")
    print(f"   Result: {result['message']}")
    assert result['success'], f"Update failed: {result}"
    
    print("\n2. Adding step to routine...")
    result = add_step_to_routine(
        "test_routine",
        action="wait",
        params={"seconds": 0.1}
    )
    print(f"   Result: {result['message']}")
    assert result['success'], f"Add step failed: {result}"
    
    print("\n3. Removing step from routine...")
    result = remove_step_from_routine("test_routine", position=0)
    print(f"   Result: {result['message']}")
    assert result['success'], f"Remove step failed: {result}"
    
    print("\n✅ Update Routine test passed!")
    return True


def test_execute_routine_dry_run():
    """Test routine execution in dry run mode."""
    print("\n" + "="*60)
    print("TESTING: Execute Routine (Dry Run)")
    print("="*60)
    
    print("\n1. Dry run of morning routine...")
    result = execute_routine("morning", dry_run=True)
    print(f"   Result: {result['message']}")
    print(f"   Steps that would execute: {result['steps_executed']}")
    assert result['success'], f"Dry run failed: {result}"
    
    print("\n2. Dry run of focus routine...")
    result = execute_routine("focus", dry_run=True)
    print(f"   Result: {result['message']}")
    assert result['success'], f"Dry run failed: {result}"
    
    print("\n✅ Execute Routine (Dry Run) test passed!")
    return True


def test_execute_routine_simple():
    """Test actual routine execution with simple steps."""
    print("\n" + "="*60)
    print("TESTING: Execute Routine (Simple)")
    print("="*60)
    
    # Create a simple routine with just wait and notify
    print("\n1. Creating simple test routine...")
    create_routine(
        name="simple_test",
        steps=[
            {"action": "wait", "params": {"seconds": 0.5}},
        ],
        description="Simple test with wait only"
    )
    
    print("\n2. Executing simple test routine...")
    result = execute_routine("simple_test")
    print(f"   Result: {result['message']}")
    assert result['success'], f"Execute failed: {result}"
    
    # Clean up
    delete_routine("simple_test")
    
    print("\n✅ Execute Routine (Simple) test passed!")
    return True


def test_delete_routine():
    """Test deleting a routine."""
    print("\n" + "="*60)
    print("TESTING: Delete Routine")
    print("="*60)
    
    print("\n1. Deleting test routine...")
    result = delete_routine("test_routine")
    print(f"   Result: {result['message']}")
    assert result['success'], f"Delete failed: {result}"
    
    print("\n2. Verifying deletion...")
    result = get_routine("test_routine")
    assert not result['success'], "Routine should not exist after deletion"
    print("   Confirmed: routine no longer exists")
    
    print("\n✅ Delete Routine test passed!")
    return True


def run_all_tests():
    """Run all Tier 3 tests."""
    print("\n" + "#"*60)
    print("#" + " "*20 + "SAGE TIER 3 TESTS" + " "*21 + "#")
    print("#" + " "*18 + "Custom Routines" + " "*25 + "#")
    print("#"*60)
    
    tests = [
        ("Create Routine", test_create_routine),
        ("Get Routine", test_get_routine),
        ("List Routines", test_list_routines),
        ("Update Routine", test_update_routine),
        ("Execute Routine (Dry Run)", test_execute_routine_dry_run),
        ("Execute Routine (Simple)", test_execute_routine_simple),
        ("Delete Routine", test_delete_routine),
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
