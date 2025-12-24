# SAGE Interview Preparation Guide

> A comprehensive technical deep-dive for explaining this project in interviews.

---

## 1. The "Elevator Pitch" Architecture

### System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SAGE VOICE ASSISTANT                               │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────┐
                              │   USER       │
                              │  (Voice/Text)│
                              └──────┬───────┘
                                     │
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
           ┌───────────────┐                ┌───────────────┐
           │  WAKE WORD    │                │  TEXT INPUT   │
           │  (Picovoice)  │                │  (Tkinter)    │
           │  "Hey Siri"   │                │               │
           └───────┬───────┘                └───────┬───────┘
                   │                                │
                   ▼                                │
           ┌───────────────┐                        │
           │  SPEECH-TO-   │                        │
           │  TEXT (Google │                        │
           │  Web Speech)  │                        │
           └───────┬───────┘                        │
                   │                                │
                   └────────────────┬───────────────┘
                                    ▼
                          ┌─────────────────┐
                          │  TASK EXECUTOR  │
                          │  (Wrapper)      │
                          └────────┬────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  ORCHESTRATOR   │
                          │  (Groq Llama    │
                          │   3.3 70B)      │
                          │                 │
                          │  JSON Mode for  │
                          │  Tool Calling   │
                          └────────┬────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
     ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
     │  40+ BUILT-IN  │   │  CODE          │   │  DIRECT        │
     │  TOOLS         │   │  GENERATOR     │   │  RESPONSE      │
     │                │   │  (OpenRouter   │   │  (No tool      │
     │  • System      │   │   Qwen 2.5)    │   │   needed)      │
     │  • Productivity│   │                │   │                │
     │  • Communication│  │  Auto-creates  │   │  "What is      │
     │  • AI/Media    │   │  PyAutoGUI     │   │   quantum      │
     └────────┬───────┘   │  tools         │   │   computing?"  │
              │           └────────┬───────┘   └────────┬───────┘
              │                    │                    │
              └────────────────────┼────────────────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  TEXT-TO-SPEECH │
                          │  (pyttsx3/SAPI) │
                          └────────┬────────┘
                                   │
                                   ▼
                              ┌──────────┐
                              │   USER   │
                              │ (Hears   │
                              │ Response)│
                              └──────────┘
```

### Component Communication

| Component | File | Talks To | Purpose |
|-----------|------|----------|---------|
| `main.py` | Entry point | `ui/`, `core/` | Starts GUI or CLI mode |
| `ParticleWindow` | `ui/particle_window.py` | `TaskExecutor`, `voice/` | GUI with voice loop |
| `TaskExecutor` | `core/task_executor.py` | `OrchestratorAgent` | Thin wrapper for execution |
| `OrchestratorAgent` | `core/orchestrator.py` | `tools/`, `CodeGenerator` | Brain - decides which tools to call |
| `CodeGeneratorAgent` | `core/code_generator.py` | OpenRouter API | Creates new tools on-the-fly |
| `WakeWordDetector` | `voice/wake_word.py` | `SpeechToText` | Listens for "Hey Siri" |
| `SpeechToText` | `voice/speech_to_text.py` | `TaskExecutor` | Converts voice to text |
| `TTSEngine` | `voice/tts.py` | User (speaker) | Speaks responses aloud |

---

## 2. Tech Stack Defense (The "Why")

### Core Libraries

| Library | Why This? | Alternatives Considered |
|---------|-----------|------------------------|
| **Groq** | 10x faster inference than OpenAI. Free tier. JSON mode for reliable tool calling. | OpenAI (slower, expensive), Ollama (local but slower) |
| **pvporcupine** (Picovoice) | On-device wake word detection. Low latency (<100ms). Works offline. | Snowboy (deprecated), Pocketsphinx (less accurate) |
| **speech_recognition** | Simple API, Google Web Speech is free and accurate. | Whisper (requires GPU), DeepSpeech (complex setup) |
| **pyttsx3** | Uses Windows SAPI - no API calls, works offline, zero latency. | gTTS (requires internet), ElevenLabs (expensive) |
| **pyautogui** | Cross-platform desktop automation. Simple API for clicks/typing. | pywinauto (Windows only), Selenium (web only) |
| **tkinter** | Built into Python - no extra dependencies. Fast for simple UIs. | PyQt (heavy), Electron (overkill) |

### Why NOT LangChain?

**Common Interview Question:** "Why didn't you use LangChain for the agent?"

**Answer:**
```
LangChain adds complexity we don't need. Our orchestrator is ~300 lines of code that:
1. Sends a system prompt with tool descriptions to Groq
2. Gets back JSON with tool_calls array
3. Executes tools in sequence

LangChain would add:
- 50+ dependencies
- Abstraction layers that hide what's happening
- Harder to debug when things go wrong

For a desktop assistant with 40 tools, direct API calls are simpler and faster.
```

### Why Groq over OpenAI?

```
1. Speed: Groq runs Llama 3.3 70B at ~500 tokens/sec vs OpenAI's ~50 tokens/sec
2. Cost: Free tier with 30 requests/minute
3. JSON Mode: Native support for structured output (no function calling overhead)
4. Open Model: Llama 3.3 is open-source, no vendor lock-in
```

---

## 3. Code Deep Dive (The "How")

### Function #1: `orchestrate()` - The Brain

**File:** `core/orchestrator.py` (lines 240-330)

```python
def orchestrate(self, user_input: str) -> Dict[str, Any]:
```

**What it does:** Takes natural language input, decides which tools to call, executes them.

**Line-by-line breakdown:**

```python
# 1. Check if API is available
if not self.client:
    return {'success': False, 'message': 'Orchestrator offline'}

# 2. Build system prompt with all 40+ tools
tools_desc = self.get_tools_description()
system_prompt = f"""You are SAGE... Available tools: {tools_desc}
Respond with JSON only: {{"tool_calls": [...], "response": "..."}}"""

# 3. Call Groq with JSON mode (forces valid JSON output)
response = self.client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ],
    response_format={"type": "json_object"},  # KEY: Forces JSON
    temperature=0.1  # Low = consistent tool selection
)

# 4. Parse JSON and execute tools
parsed = json.loads(response.choices[0].message.content)

# 5. If needs automation (no existing tool), generate one
if parsed.get('needs_automation', False):
    return self._handle_automation_request(user_input, parsed)

# 6. Execute the planned tools
return self._execute_plan(parsed, user_input)
```

**Input:** `"open chrome and set volume to 50"`

**Output:**
```json
{
  "success": true,
  "tool_calls": [
    {"tool": "open_app", "params": {"app_name": "chrome"}, "result": {...}},
    {"tool": "set_volume", "params": {"level": 50}, "result": {...}}
  ],
  "response": "Opened Chrome and set volume to 50%"
}
```

---

### Function #2: `_execute_plan()` - The Executor

**File:** `core/orchestrator.py` (lines 780-880)

```python
def _execute_plan(self, plan: Dict[str, Any], original_input: str) -> Dict[str, Any]:
```

**What it does:** Takes the LLM's plan and executes each tool in sequence, passing data between steps.

**Key mechanism - Step Memory:**

```python
# Memory for passing data between steps
step_memory = {}

for tool_call in plan['tool_calls']:
    # Resolve variables like $CONTENT_FROM_PREVIOUS_STEP
    params = self._resolve_params(params, step_memory)
    
    # Execute tool
    result = tool_function(**params)
    
    # Store result for next step
    if 'content' in result:
        step_memory['CONTENT_FROM_PREVIOUS_STEP'] = result['content']
```

**Example flow for "send birthday invitation to Sujal":**

```
Step 1: generate_content(topic="birthday invitation") 
        → Returns: {"content": "Hey! You're invited to my birthday..."}
        → Stored in step_memory['CONTENT_FROM_PREVIOUS_STEP']

Step 2: send_whatsapp(contact="Sujal", message="$CONTENT_FROM_PREVIOUS_STEP")
        → $CONTENT_FROM_PREVIOUS_STEP resolved to actual content
        → WhatsApp opens with message typed
```

---

### Function #3: `_handle_rate_limit()` - The Fallback

**File:** `core/orchestrator.py` (lines 950-1150)

```python
def _handle_rate_limit(self, user_input: str) -> Dict[str, Any]:
```

**What it does:** When Groq API hits rate limit (429 error), uses pattern matching to handle common commands without AI.

**Why this matters:** Shows defensive programming - the assistant doesn't just fail, it degrades gracefully.

```python
# Pattern matching for common commands
user_lower = user_input.lower()

# Volume commands - extract number with regex
if "volume" in user_lower:
    volume_match = re.search(r'(\d+)', user_input)
    if volume_match:
        level = int(volume_match.group(1))
        from tools.system.volume import set_volume
        return set_volume(level)

# Time commands - direct tool call
if any(word in user_lower for word in ["time", "clock"]):
    from tools.productivity.datetime_tool import get_time
    return get_time()

# Calculator - parse math expressions
if "calculate" in user_lower:
    # Regex to extract "5 plus 3" or "5 + 3"
    math_pattern = r'(\d+)\s*(?:plus|\+|times|\*|minus|-)\s*(\d+)'
    match = re.search(math_pattern, user_lower)
    # ... perform calculation
```

**Supported fallback commands:**
- `open [app]` - Opens Chrome, Notepad, etc.
- `volume [0-100]` - Sets system volume
- `what time is it` - Returns current time
- `weather in [city]` - Gets weather
- `calculate [expression]` - Basic math
- `type [text]` - Types on screen
- `find [file] in downloads` - Searches downloads folder

---

## 4. Error Handling & Edge Cases

### Error Handling Locations

| Location | What It Protects | How |
|----------|------------------|-----|
| `orchestrate()` | API failures, JSON parse errors | try-except with specific handlers |
| `_execute_plan()` | Individual tool failures | Per-tool try-except, continues to next |
| `_handle_rate_limit()` | 429 errors | Pattern-matching fallback |
| `voice/wake_word.py` | Microphone errors | Graceful cleanup in finally block |
| `voice/tts.py` | Speech engine failures | Thread lock prevents race conditions |
| `code_generator.py` | Dangerous code generation | Safety check before execution |

### Key Try-Except Blocks

**1. Orchestrator - API Call Protection:**
```python
# core/orchestrator.py, line 310
try:
    response = self.client.chat.completions.create(...)
    parsed = json.loads(content)
except json.JSONDecodeError as e:
    return {'success': False, 'message': f'Failed to parse: {e}'}
except Exception as e:
    if "429" in str(e):
        return self._handle_rate_limit(user_input)  # Graceful fallback
    return {'success': False, 'message': f'Error: {e}'}
```

**2. Tool Execution - Per-Tool Isolation:**
```python
# core/orchestrator.py, line 850
for tool_call in plan['tool_calls']:
    try:
        result = tool_function(**params)
        results['tool_calls'].append({'tool': tool_name, 'result': result})
    except Exception as e:
        # Log error but continue to next tool
        results['execution_log'].append({'status': 'error', 'error': str(e)})
        results['success'] = False
        continue  # Don't stop entire execution
```

**3. Code Generator - Safety Check:**
```python
# core/code_generator.py, line 180
dangerous_operations = ['shutdown', 'delete', 'rm ', 'format', 'registry']

def _check_code_safety(self, code: str) -> Dict[str, Any]:
    code_lower = code.lower()
    found_issues = []
    for dangerous_op in self.dangerous_operations:
        if dangerous_op in code_lower:
            found_issues.append(dangerous_op)
    return {'safe': len(found_issues) == 0, 'issues': found_issues}
```

**4. TTS - Thread Safety:**
```python
# voice/tts.py, line 45
def speak(self, text: str):
    def speak_thread():
        with self._lock:  # Prevents multiple speeches overlapping
            self.speaking = True
            try:
                engine = self._get_engine()
                engine.say(text)
                engine.runAndWait()
            finally:
                self.speaking = False
```

### Edge Cases Handled

| Edge Case | How It's Handled |
|-----------|------------------|
| No API key | Returns "Orchestrator offline" message |
| Rate limit (429) | Falls back to pattern matching |
| Unknown tool name | Logs error, continues to next tool |
| Microphone not found | Catches PyAudio error, shows hint |
| No speech detected | Returns empty string, prompts retry |
| Dangerous generated code | Blocks execution, requires approval |
| TTS engine crash | Creates fresh engine per speech |

---

## 5. Mock Interview Q&A

### Q1: "How does the agent decide which tool to use?"

**Answer:**
```
The orchestrator sends a system prompt to Groq Llama 3.3 that contains:
1. A list of all 40+ available tools with their descriptions and parameters
2. Instructions to respond in JSON format with a "tool_calls" array

The LLM analyzes the user's intent and returns JSON like:
{
  "thinking": "User wants to open Chrome and adjust volume",
  "tool_calls": [
    {"tool": "open_app", "params": {"app_name": "chrome"}},
    {"tool": "set_volume", "params": {"level": 50}}
  ]
}

We use JSON mode (response_format={"type": "json_object"}) which forces 
the model to output valid JSON, eliminating parsing errors.

Temperature is set to 0.1 for consistent tool selection.
```

---

### Q2: "What happens if a tool doesn't exist for the user's request?"

**Answer:**
```
The orchestrator has a "needs_automation" flag. If the LLM determines no 
existing tool can handle the request but it could be automated with 
mouse/keyboard actions, it sets needs_automation: true.

This triggers the CodeGeneratorAgent which:
1. Calls OpenRouter API with Qwen 2.5 Coder model
2. Generates PyAutoGUI code for the task
3. Runs safety checks (blocks dangerous operations like 'delete', 'shutdown')
4. Saves the generated tool to data/generated_tools/ for reuse
5. Executes the tool

Example: "Click the save button in Notepad" would generate:
- pyautogui.locateOnScreen('save_button.png')
- pyautogui.click(location)
```

---

### Q3: "How do you handle multi-step tasks where one tool's output feeds into another?"

**Answer:**
```
We use a "step_memory" dictionary that persists across tool executions.

When a tool returns data (like generate_content returning text), we store it:
  step_memory['CONTENT_FROM_PREVIOUS_STEP'] = result['content']

In subsequent tool calls, parameters can reference this with $VARIABLE_NAME:
  {"tool": "send_whatsapp", "params": {"message": "$CONTENT_FROM_PREVIOUS_STEP"}}

The _resolve_params() function replaces these variables before execution:
  if value.startswith('$'):
      var_name = value[1:]
      resolved[key] = memory.get(var_name, value)

This enables chains like:
1. generate_content → produces invitation text
2. send_whatsapp → uses that text as the message
```

---

### Q4: "Why use Picovoice for wake word instead of always-on speech recognition?"

**Answer:**
```
Three reasons:

1. Privacy: Picovoice runs entirely on-device. Audio never leaves the computer.
   Always-on Google STT would stream all audio to Google's servers.

2. Efficiency: Wake word detection uses ~5% CPU vs ~30% for continuous STT.
   It's designed to run 24/7 without draining battery.

3. Latency: Picovoice detects "Hey Siri" in <100ms. 
   Continuous STT would need to process all audio, adding delay.

The flow is:
- Picovoice listens for wake word (low power, on-device)
- Only after detection do we activate Google STT (high accuracy, cloud)
- This gives us the best of both worlds
```

---

### Q5: "How would you scale this to handle multiple users or run as a service?"

**Answer:**
```
Current architecture is single-user desktop app. To scale:

1. Separate the orchestrator into a REST API:
   - FastAPI server with /orchestrate endpoint
   - Each request gets its own step_memory (stateless)
   - Rate limiting per user/API key

2. Replace local tools with remote execution:
   - System tools (volume, apps) → Remote desktop protocol
   - Communication tools → OAuth-based APIs (Gmail API, WhatsApp Business)

3. Voice handling:
   - WebSocket connection for streaming audio
   - Server-side STT (Whisper) instead of client Google STT
   - TTS audio streamed back to client

4. State management:
   - Redis for session state (step_memory, conversation history)
   - PostgreSQL for user preferences and generated tools

5. Scaling:
   - Kubernetes for orchestrator pods
   - Queue (RabbitMQ) for tool execution jobs
   - Separate workers for CPU-intensive tasks (code generation)

The core orchestration logic (JSON tool calling) stays the same - 
it's already stateless per request.
```

---

## Quick Reference Card

### Key Files to Know
- `core/orchestrator.py` - Main AI logic (1300 lines)
- `core/code_generator.py` - Auto tool generation
- `ui/particle_window.py` - GUI with voice loop
- `voice/wake_word.py` - Picovoice integration
- `voice/tts.py` - Text-to-speech

### Key Functions to Explain
- `orchestrate()` - Analyzes input, calls LLM, returns tool plan
- `_execute_plan()` - Runs tools in sequence with step memory
- `_handle_rate_limit()` - Pattern-matching fallback
- `generate_tool()` - Creates PyAutoGUI code on-the-fly

### Numbers to Remember
- 40+ built-in tools
- Groq Llama 3.3 70B model
- ~500 tokens/sec inference speed
- <100ms wake word detection
- 0.1 temperature for consistent tool selection

---

*Good luck with your interview! 🚀*
