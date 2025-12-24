"""
Orchestration Test - Compare Groq vs Gemini for tool calling
Tests both providers with real-world agentic tasks
"""

import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

# ============================================
# TOOL DEFINITIONS (same for both)
# ============================================

TOOLS = [
    {
        "name": "open_app",
        "description": "Open an application by name",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Name of app to open (e.g., 'chrome', 'notepad')"}
            },
            "required": ["app_name"]
        }
    },
    {
        "name": "send_whatsapp",
        "description": "Send a WhatsApp message to a contact",
        "parameters": {
            "type": "object",
            "properties": {
                "contact_name": {"type": "string", "description": "Name of the contact"},
                "message": {"type": "string", "description": "Message to send"}
            },
            "required": ["contact_name", "message"]
        }
    },
    {
        "name": "search_web",
        "description": "Search the web for information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "set_volume",
        "description": "Set system volume level",
        "parameters": {
            "type": "object",
            "properties": {
                "level": {"type": "integer", "description": "Volume level 0-100"}
            },
            "required": ["level"]
        }
    },
    {
        "name": "send_email",
        "description": "Send an email",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Recipient email"},
                "subject": {"type": "string", "description": "Email subject"},
                "body": {"type": "string", "description": "Email body"}
            },
            "required": ["to", "subject", "body"]
        }
    },
    {
        "name": "get_weather",
        "description": "Get weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "calculate",
        "description": "Perform mathematical calculation",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression to evaluate"}
            },
            "required": ["expression"]
        }
    },
    {
        "name": "create_file",
        "description": "Create a new file with content",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Name of file to create"},
                "content": {"type": "string", "description": "Content to write"}
            },
            "required": ["filename", "content"]
        }
    }
]

# Test cases - real world orchestration scenarios
TEST_CASES = [
    # Simple single tool
    "open chrome",
    "set volume to 30",
    
    # Needs understanding
    "message sujal on whatsapp saying hey bro whats up",
    "find information about python asyncio",
    
    # Multi-step (should return multiple tools or a plan)
    "search for today's weather in mumbai and send it to raj on whatsapp",
    "open notepad and also set volume to 50",
    
    # Ambiguous - tests reasoning
    "remind me to call mom",  # No direct tool - should it create a file? or say no tool?
    "play some music",  # Could be open spotify or search
]

# ============================================
# GROQ TEST (Native Tool Calling)
# ============================================

def test_groq_native():
    """Test Groq with native tool calling"""
    from groq import Groq
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    results = []
    
    # Convert our tools to Groq format
    groq_tools = []
    for tool in TOOLS:
        groq_tools.append({
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
        })
    
    print("\n" + "="*60)
    print("GROQ - Native Tool Calling (Llama 3.3 70B)")
    print("="*60)
    
    for test in TEST_CASES:
        print(f"\n📝 Input: {test}")
        try:
            start = time.time()
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a desktop assistant. Use the provided tools to help the user. If multiple tools are needed, call them in sequence."},
                    {"role": "user", "content": test}
                ],
                tools=groq_tools,
                tool_choice="auto"
            )
            elapsed = time.time() - start
            
            msg = response.choices[0].message
            if msg.tool_calls:
                for tc in msg.tool_calls:
                    print(f"   ✅ Tool: {tc.function.name}")
                    print(f"      Args: {tc.function.arguments}")
            else:
                print(f"   💬 Response: {msg.content[:100]}...")
            print(f"   ⏱️  Time: {elapsed:.2f}s")
            
            results.append({
                "input": test,
                "tool_calls": [{"name": tc.function.name, "args": tc.function.arguments} for tc in (msg.tool_calls or [])],
                "response": msg.content if not msg.tool_calls else None,
                "time": elapsed
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({"input": test, "error": str(e)})
        
        time.sleep(2)  # Rate limit
    
    return results

# ============================================
# GROQ TEST (JSON Mode - Manual Parsing)
# ============================================

def test_groq_json():
    """Test Groq with JSON mode (manual tool parsing)"""
    from groq import Groq
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    results = []
    
    tools_desc = "\n".join([f"- {t['name']}: {t['description']} | params: {list(t['parameters']['properties'].keys())}" for t in TOOLS])
    
    system_prompt = f"""You are a desktop assistant. Analyze the user request and decide which tools to call.

Available tools:
{tools_desc}

Respond with JSON only:
{{
    "thinking": "brief reasoning",
    "tool_calls": [
        {{"tool": "tool_name", "params": {{"param1": "value1"}}}}
    ]
}}

If no tool matches, set tool_calls to empty array and add "response" field with your answer."""

    print("\n" + "="*60)
    print("GROQ - JSON Mode (Manual Parsing)")
    print("="*60)
    
    for test in TEST_CASES:
        print(f"\n📝 Input: {test}")
        try:
            start = time.time()
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": test}
                ],
                response_format={"type": "json_object"}
            )
            elapsed = time.time() - start
            
            content = response.choices[0].message.content
            parsed = json.loads(content)
            
            if parsed.get("tool_calls"):
                for tc in parsed["tool_calls"]:
                    print(f"   ✅ Tool: {tc['tool']}")
                    print(f"      Args: {tc['params']}")
            if parsed.get("response"):
                print(f"   💬 Response: {parsed['response'][:100]}...")
            if parsed.get("thinking"):
                print(f"   🧠 Thinking: {parsed['thinking'][:80]}...")
            print(f"   ⏱️  Time: {elapsed:.2f}s")
            
            results.append({
                "input": test,
                "parsed": parsed,
                "time": elapsed
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({"input": test, "error": str(e)})
        
        time.sleep(2)
    
    return results

# ============================================
# GEMINI TEST (Native Tool Calling)
# ============================================

def test_gemini_native():
    """Test Gemini with native function calling"""
    import google.generativeai as genai
    
    # Get first available Gemini key
    gemini_key = os.getenv("GEMINI_API_KEY_1") or os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("❌ No Gemini API key found")
        return []
    
    genai.configure(api_key=gemini_key)
    
    # Convert tools to Gemini format
    gemini_tools = []
    for tool in TOOLS:
        gemini_tools.append(
            genai.protos.Tool(
                function_declarations=[
                    genai.protos.FunctionDeclaration(
                        name=tool["name"],
                        description=tool["description"],
                        parameters=genai.protos.Schema(
                            type=genai.protos.Type.OBJECT,
                            properties={
                                k: genai.protos.Schema(type=genai.protos.Type.STRING, description=v.get("description", ""))
                                for k, v in tool["parameters"]["properties"].items()
                            },
                            required=tool["parameters"].get("required", [])
                        )
                    )
                ]
            )
        )
    
    model = genai.GenerativeModel('gemini-2.5-flash', tools=gemini_tools)
    results = []
    
    print("\n" + "="*60)
    print("GEMINI - Native Function Calling (1.5 Flash)")
    print("="*60)
    
    for test in TEST_CASES:
        print(f"\n📝 Input: {test}")
        try:
            start = time.time()
            response = model.generate_content(test)
            elapsed = time.time() - start
            
            # Check for function calls
            if response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        fc = part.function_call
                        print(f"   ✅ Tool: {fc.name}")
                        print(f"      Args: {dict(fc.args)}")
                    elif hasattr(part, 'text') and part.text:
                        print(f"   💬 Response: {part.text[:100]}...")
            print(f"   ⏱️  Time: {elapsed:.2f}s")
            
            results.append({
                "input": test,
                "response": str(response.candidates[0].content),
                "time": elapsed
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({"input": test, "error": str(e)})
        
        time.sleep(4)  # Gemini has stricter rate limits
    
    return results

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("🧪 ORCHESTRATION TEST - Comparing LLM Providers")
    print("Testing tool calling capabilities for agentic workflows\n")
    
    # Run tests
    groq_native_results = test_groq_native()
    
    print("\n" + "="*60)
    print("Waiting 10s before next test (rate limits)...")
    print("="*60)
    time.sleep(10)
    
    groq_json_results = test_groq_json()
    
    print("\n" + "="*60)
    print("Waiting 10s before Gemini test...")
    print("="*60)
    time.sleep(10)
    
    gemini_results = test_gemini_native()
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    print(f"Groq Native: {len([r for r in groq_native_results if 'error' not in r])}/{len(TEST_CASES)} successful")
    print(f"Groq JSON:   {len([r for r in groq_json_results if 'error' not in r])}/{len(TEST_CASES)} successful")
    print(f"Gemini:      {len([r for r in gemini_results if 'error' not in r])}/{len(TEST_CASES)} successful")
