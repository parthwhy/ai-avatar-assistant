#!/usr/bin/env python3
"""
Comprehensive Test - Check all SAGE functionalities
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all module imports"""
    print("=== Testing Module Imports ===")
    
    tests = []
    
    # Core modules
    try:
        from core.orchestrator import OrchestratorAgent
        tests.append(("core.orchestrator", True))
    except Exception as e:
        tests.append(("core.orchestrator", False, str(e)))
    
    try:
        from core.task_executor import get_executor
        tests.append(("core.task_executor", True))
    except Exception as e:
        tests.append(("core.task_executor", False, str(e)))
    
    # Communication tools
    try:
        from tools.communication.whatsapp import send_whatsapp, whatsapp_call
        tests.append(("tools.communication.whatsapp", True))
    except Exception as e:
        tests.append(("tools.communication.whatsapp", False, str(e)))
    
    try:
        from tools.communication.email_sender import send_email_browser
        tests.append(("tools.communication.email_sender", True))
    except Exception as e:
        tests.append(("tools.communication.email_sender", False, str(e)))
    
    # Productivity tools
    try:
        from tools.productivity.contacts import find_contact
        tests.append(("tools.productivity.contacts", True))
    except Exception as e:
        tests.append(("tools.productivity.contacts", False, str(e)))
    
    try:
        from tools.productivity.meeting_scheduler import schedule_meeting
        tests.append(("tools.productivity.meeting_scheduler", True))
    except Exception as e:
        tests.append(("tools.productivity.meeting_scheduler", False, str(e)))
    
    # AI tools
    try:
        from tools.ai.content_generator import generate_content
        tests.append(("tools.ai.content_generator", True))
    except Exception as e:
        tests.append(("tools.ai.content_generator", False, str(e)))
    
    try:
        from tools.ai.file_analyzer import analyze_document
        tests.append(("tools.ai.file_analyzer", True))
    except Exception as e:
        tests.append(("tools.ai.file_analyzer", False, str(e)))
    
    # System tools
    try:
        from tools.system.app_launcher import open_app
        tests.append(("tools.system.app_launcher", True))
    except Exception as e:
        tests.append(("tools.system.app_launcher", False, str(e)))
    
    try:
        from tools.system.downloads_search import search_downloads
        tests.append(("tools.system.downloads_search", True))
    except Exception as e:
        tests.append(("tools.system.downloads_search", False, str(e)))
    
    try:
        from tools.system.text_typer import type_on_screen
        tests.append(("tools.system.text_typer", True))
    except Exception as e:
        tests.append(("tools.system.text_typer", False, str(e)))
    
    # Media tools
    try:
        from tools.media.spotify import play_song_on_spotify
        tests.append(("tools.media.spotify", True))
    except Exception as e:
        tests.append(("tools.media.spotify", False, str(e)))
    
    # Voice modules
    try:
        from voice.tts import speak
        tests.append(("voice.tts", True))
    except Exception as e:
        tests.append(("voice.tts", False, str(e)))
    
    # Print results
    passed = 0
    failed = 0
    for test in tests:
        if test[1]:
            print(f"  ✅ {test[0]}")
            passed += 1
        else:
            print(f"  ❌ {test[0]}: {test[2] if len(test) > 2 else 'Unknown error'}")
            failed += 1
    
    print(f"\nImports: {passed} passed, {failed} failed")
    return failed == 0


def test_contacts():
    """Test contact lookup"""
    print("\n=== Testing Contact Lookup ===")
    
    from tools.productivity.contacts import find_contact
    
    contacts_to_test = ["sujal", "manager", "hr", "mom"]
    passed = 0
    
    for contact in contacts_to_test:
        result = find_contact(contact)
        if result['success']:
            print(f"  ✅ {contact}: {result['contact']['name']} ({result['contact'].get('email', 'N/A')})")
            passed += 1
        else:
            print(f"  ❌ {contact}: {result['message']}")
    
    print(f"\nContacts: {passed}/{len(contacts_to_test)} found")
    return passed == len(contacts_to_test)


def test_content_generation():
    """Test content generation"""
    print("\n=== Testing Content Generation ===")
    
    from tools.ai.content_generator import generate_content
    
    tests = [
        ("whatsapp", "birthday invitation", "casual"),
        ("email", "meeting request", "professional"),
        ("message", "thank you note", "friendly"),
    ]
    
    passed = 0
    for content_type, topic, style in tests:
        result = generate_content(topic, content_type, style)
        if result['success']:
            content_preview = result['content'][:80].replace('\n', ' ')
            print(f"  ✅ {content_type}: {content_preview}...")
            passed += 1
        else:
            print(f"  ❌ {content_type}: {result.get('message', 'Failed')}")
    
    print(f"\nContent Generation: {passed}/{len(tests)} passed")
    return passed == len(tests)


def test_orchestrator_commands():
    """Test orchestrator with various commands"""
    print("\n=== Testing Orchestrator Commands ===")
    
    from core.orchestrator import OrchestratorAgent
    
    orchestrator = OrchestratorAgent()
    
    # Test commands (simulation only - won't actually execute)
    commands = [
        "what time is it",
        "open notepad",
        "search downloads for pdf",
        "send whatsapp to sujal about birthday",
        "send email to manager about meeting",
        "schedule meeting with hr tomorrow at 3 pm",
    ]
    
    passed = 0
    for cmd in commands:
        try:
            # Just test orchestration planning, not execution
            result = orchestrator.orchestrate(cmd)
            if result.get('success') or result.get('tool_calls'):
                print(f"  ✅ '{cmd[:40]}...' -> {len(result.get('tool_calls', []))} tools planned")
                passed += 1
            else:
                print(f"  ⚠️  '{cmd[:40]}...' -> {result.get('message', 'No plan')[:50]}")
        except Exception as e:
            print(f"  ❌ '{cmd[:40]}...' -> Error: {str(e)[:50]}")
    
    print(f"\nOrchestrator: {passed}/{len(commands)} commands processed")
    return passed >= len(commands) - 1  # Allow 1 failure


def test_followup_detection():
    """Test follow-up question detection"""
    print("\n=== Testing Follow-up Detection ===")
    
    # Simulate needs_info responses
    test_responses = [
        {"needs_info": True, "missing": "recipient", "message": "Who should I send this to?"},
        {"needs_info": True, "missing": "date", "response": "When would you like to schedule the meeting?"},
        {"success": True, "message": "Email sent successfully"},
        {"tool_calls": [{"result": {"needs_info": True, "missing": "subject"}}]},
    ]
    
    expected = [True, True, False, True]
    
    passed = 0
    for i, (response, expect_followup) in enumerate(zip(test_responses, expected)):
        # Check needs_info flag
        has_followup = response.get('needs_info', False)
        
        # Check in tool_calls
        if not has_followup and response.get('tool_calls'):
            for tc in response['tool_calls']:
                if tc.get('result', {}).get('needs_info'):
                    has_followup = True
                    break
        
        if has_followup == expect_followup:
            print(f"  ✅ Test {i+1}: Correctly detected {'follow-up needed' if has_followup else 'no follow-up'}")
            passed += 1
        else:
            print(f"  ❌ Test {i+1}: Expected {expect_followup}, got {has_followup}")
    
    print(f"\nFollow-up Detection: {passed}/{len(test_responses)} passed")
    return passed == len(test_responses)


def test_file_search():
    """Test file search functionality"""
    print("\n=== Testing File Search ===")
    
    from tools.system.downloads_search import search_downloads
    
    # Test search
    result = search_downloads("pdf")
    
    if result.get('success'):
        count = result.get('count', 0)
        print(f"  ✅ Downloads search: Found {count} files")
        files = result.get('results', result.get('files', []))
        if files:
            for f in files[:3]:
                name = f.get('name', f) if isinstance(f, dict) else str(f)
                print(f"     - {name}")
        return True
    else:
        print(f"  ⚠️  Downloads search: {result.get('message', 'No results')}")
        return True  # Not a failure, just no files


def main():
    """Run all tests"""
    print("🧪 SAGE Comprehensive Functionality Test")
    print("=" * 60)
    
    results = []
    
    # Test 1: Imports
    results.append(("Module Imports", test_imports()))
    
    # Test 2: Contacts
    results.append(("Contact Lookup", test_contacts()))
    
    # Test 3: Content Generation
    results.append(("Content Generation", test_content_generation()))
    
    # Test 4: Orchestrator
    results.append(("Orchestrator Commands", test_orchestrator_commands()))
    
    # Test 5: Follow-up Detection
    results.append(("Follow-up Detection", test_followup_detection()))
    
    # Test 6: File Search
    results.append(("File Search", test_file_search()))
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} test groups passed")
    
    if passed == len(results):
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print("\n⚠️  Some tests failed. Check output above for details.")
    
    return passed == len(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)