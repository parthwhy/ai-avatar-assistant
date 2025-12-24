#!/usr/bin/env python3
"""
Test Communication Orchestrator - Test WhatsApp and Email via Orchestrator
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import OrchestratorAgent

def test_whatsapp_orchestrator():
    """Test WhatsApp message via orchestrator"""
    print("=== Testing WhatsApp via Orchestrator ===")
    
    try:
        orchestrator = OrchestratorAgent()
        
        # Test command
        command = "send whatsapp message to sujal about my birthday"
        print(f"Command: '{command}'")
        
        result = orchestrator.orchestrate(command)
        print(f"Result: {result}")
        
        if result['success']:
            print(f"✅ Orchestrator processed WhatsApp command successfully")
            print(f"Response: {result['response']}")
            return True
        else:
            print(f"❌ Orchestrator failed: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_email_orchestrator():
    """Test email via orchestrator"""
    print("\n=== Testing Email via Orchestrator ===")
    
    try:
        orchestrator = OrchestratorAgent()
        
        # Test command
        command = "send email to manager about my birthday party"
        print(f"Command: '{command}'")
        
        result = orchestrator.orchestrate(command)
        print(f"Result: {result}")
        
        if result['success']:
            print(f"✅ Orchestrator processed email command successfully")
            print(f"Response: {result['response']}")
            return True
        else:
            print(f"❌ Orchestrator failed: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run orchestrator tests"""
    print("🧪 Testing Communication via Orchestrator")
    print("=" * 50)
    
    whatsapp_ok = test_whatsapp_orchestrator()
    email_ok = test_email_orchestrator()
    
    print("\n" + "=" * 50)
    print("🎯 ORCHESTRATOR TEST SUMMARY")
    print("=" * 50)
    print(f"✅ WhatsApp Orchestrator: {'PASS' if whatsapp_ok else 'FAIL'}")
    print(f"✅ Email Orchestrator: {'PASS' if email_ok else 'FAIL'}")
    
    if whatsapp_ok and email_ok:
        print("\n🎉 ALL ORCHESTRATOR TESTS PASSED!")

if __name__ == "__main__":
    main()