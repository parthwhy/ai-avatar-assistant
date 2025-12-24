"""
Orchestrator Agent - Agentic System Core
Uses Groq with JSON mode for reliable tool calling and multi-step workflows.
"""

import json
import time
from typing import Dict, List, Any, Optional
from groq import Groq
from config.settings import settings


class OrchestratorAgent:
    """
    Main orchestrator that breaks down user requests into tool calls.
    Uses Groq Llama 3.3 with JSON mode for reliable function calling.
    """
    
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key) if settings.groq_api_key else None
        self.model = "llama-3.3-70b-versatile"
        self.tools_registry = {}
        self.load_tools()
    
    def load_tools(self):
        """Load all available tools from the tools directory."""
        from tools import system, productivity, communication, ai, media
        from tools.productivity import datetime_tool
        
        # Register all tools with their schemas
        self.tools_registry = {
            # System tools
            "open_app": {
                "function": system.app_launcher.open_app,
                "description": "Open an application by name (chrome, notepad, etc.)",
                "parameters": ["app_name"]
            },
            "close_app": {
                "function": system.app_launcher.close_app,
                "description": "Close an application by name",
                "parameters": ["app_name"]
            },
            "type_text": {
                "function": system.app_launcher.type_text,
                "description": "Type text into the currently focused window",
                "parameters": ["text", "press_enter"]
            },
            "press_key": {
                "function": system.app_launcher.press_key,
                "description": "Press a keyboard key or combination (e.g., 'enter', 'ctrl+s')",
                "parameters": ["key"]
            },
            "set_volume": {
                "function": system.volume.set_volume,
                "description": "Set system volume level (0-100)",
                "parameters": ["level"]
            },
            "adjust_volume": {
                "function": system.volume.adjust_volume,
                "description": "Adjust volume by delta amount (+10, -10)",
                "parameters": ["delta"]
            },
            "mute": {
                "function": system.volume.mute,
                "description": "Mute system audio",
                "parameters": []
            },
            "unmute": {
                "function": system.volume.unmute,
                "description": "Unmute system audio",
                "parameters": []
            },
            "set_brightness": {
                "function": system.brightness.set_brightness,
                "description": "Set screen brightness level (0-100)",
                "parameters": ["level"]
            },
            "adjust_brightness": {
                "function": system.brightness.adjust_brightness,
                "description": "Adjust brightness by delta amount (+10, -10)",
                "parameters": ["delta"]
            },
            "lock_screen": {
                "function": system.power.lock_screen,
                "description": "Lock the computer screen",
                "parameters": []
            },
            "sleep": {
                "function": system.power.sleep,
                "description": "Put computer to sleep",
                "parameters": []
            },
            "shutdown": {
                "function": system.power.shutdown,
                "description": "Shutdown the computer",
                "parameters": []
            },
            "restart": {
                "function": system.power.restart,
                "description": "Restart the computer",
                "parameters": []
            },
            
            # Productivity tools
            "search_web": {
                "function": productivity.web_search.search_web,
                "description": "Search the web for information",
                "parameters": ["query"]
            },
            "open_url": {
                "function": productivity.web_search.open_url,
                "description": "Open a specific URL in browser",
                "parameters": ["url"]
            },
            "calculate": {
                "function": productivity.calculator.calculate,
                "description": "Perform mathematical calculations",
                "parameters": ["expression"]
            },
            "get_weather": {
                "function": productivity.weather.get_weather,
                "description": "Get weather information for a city",
                "parameters": ["city"]
            },
            "set_timer": {
                "function": productivity.timer.set_timer,
                "description": "Set a timer for specified minutes",
                "parameters": ["minutes"]
            },
            "set_reminder": {
                "function": productivity.timer.set_reminder,
                "description": "Set a reminder with text and time",
                "parameters": ["text", "minutes"]
            },
            "get_time": {
                "function": datetime_tool.get_time,
                "description": "Get current time",
                "parameters": []
            },
            "get_date": {
                "function": datetime_tool.get_date,
                "description": "Get current date",
                "parameters": []
            },
            "get_disk_space": {
                "function": productivity.system_info.get_disk_space,
                "description": "Get disk space information",
                "parameters": ["drive"]
            },
            "get_battery": {
                "function": productivity.system_info.get_battery_status,
                "description": "Get battery status (laptops)",
                "parameters": []
            },
            "search_file": {
                "function": system.file_search.search_file,
                "description": "Search for files by name on the system",
                "parameters": ["filename", "search_path", "max_results"]
            },
            "open_file_location": {
                "function": system.file_search.open_file_location,
                "description": "Open the folder containing a specific file",
                "parameters": ["filepath"]
            },
            "search_files_by_type": {
                "function": system.file_search.search_files_by_type,
                "description": "Search for files by type (document, image, video, etc.)",
                "parameters": ["file_type", "search_path", "max_results"]
            },
            "search_downloads": {
                "function": system.downloads_search.search_downloads,
                "description": "Search for files only in Downloads folder with GUI to open top 2 results",
                "parameters": ["filename"]
            },
            "type_on_screen": {
                "function": system.text_typer.type_on_screen,
                "description": "Type text on screen at current cursor position with speed control",
                "parameters": ["text", "typing_speed", "press_enter"]
            },
            "type_multiline_text": {
                "function": system.text_typer.type_multiline_text,
                "description": "Type multiple lines of text with delays between lines",
                "parameters": ["lines", "line_delay"]
            },
            "type_formatted_text": {
                "function": system.text_typer.type_formatted_text,
                "description": "Type text with formatting (uppercase, lowercase, title, sentence)",
                "parameters": ["text", "format_type"]
            },
            "clear_and_type": {
                "function": system.text_typer.clear_and_type,
                "description": "Clear current content and type new text",
                "parameters": ["text", "clear_method"]
            },
            "get_clipboard": {
                "function": productivity.clipboard.get_clipboard,
                "description": "Get clipboard content",
                "parameters": []
            },
            "find_contact": {
                "function": productivity.contacts.find_contact,
                "description": "Find contact information by name or role",
                "parameters": ["name_or_role"]
            },
            "smart_email_lookup": {
                "function": productivity.contacts.smart_email_lookup,
                "description": "Smart lookup for email preparation (e.g., 'send leave letter to manager')",
                "parameters": ["query"]
            },
            "schedule_meeting": {
                "function": productivity.meeting_scheduler.schedule_meeting,
                "description": "Schedule a Google Meet meeting with someone. Opens calendar and sends email invite. Will ask for missing date/time.",
                "parameters": ["attendee", "title", "date", "time", "duration_minutes"]
            },
            "quick_meeting": {
                "function": productivity.meeting_scheduler.quick_meeting,
                "description": "Start a quick Google Meet meeting now",
                "parameters": ["attendee"]
            },
            
            # Communication tools
            "send_email_browser": {
                "function": communication.email_sender.send_email_browser,
                "description": "Send email via browser (Gmail). Can use contact name instead of email. Will ask for missing info.",
                "parameters": ["to", "subject", "body", "recipient_name"]
            },
            "send_whatsapp": {
                "function": communication.whatsapp.send_whatsapp,
                "description": "Send WhatsApp message to contact",
                "parameters": ["contact_name", "message"]
            },
            "whatsapp_call": {
                "function": communication.whatsapp.whatsapp_call,
                "description": "Start a WhatsApp voice call with a contact",
                "parameters": ["contact_name"]
            },
            "whatsapp_video_call": {
                "function": communication.whatsapp.whatsapp_video_call,
                "description": "Start a WhatsApp video call with a contact",
                "parameters": ["contact_name"]
            },
            
            # AI tools
            "summarize": {
                "function": ai.summarizer.summarize,
                "description": "Summarize text content",
                "parameters": ["text"]
            },
            "explain_code": {
                "function": ai.code_helper.explain_code,
                "description": "Explain code functionality",
                "parameters": ["code"]
            },
            "generate_code": {
                "function": ai.code_helper.generate_code,
                "description": "Generate code for a task",
                "parameters": ["task", "language"]
            },
            "generate_content": {
                "function": ai.content_generator.generate_content,
                "description": "Generate content (document, letter, invitation, email, etc.)",
                "parameters": ["topic", "content_type", "style"]
            },
            "whats_on_screen": {
                "function": ai.screen_analyzer.whats_on_screen,
                "description": "Analyze current screen and describe what's visible, including buttons and options",
                "parameters": []
            },
            "analyze_screen": {
                "function": ai.screen_analyzer.analyze_screen,
                "description": "Analyze screen with a specific question about what's visible",
                "parameters": ["question"]
            },
            "get_screen_options": {
                "function": ai.screen_analyzer.get_screen_options,
                "description": "List all clickable buttons and options visible on screen",
                "parameters": []
            },
            "analyze_document": {
                "function": ai.file_analyzer.analyze_document,
                "description": "Find and analyze a document (PDF, TXT, etc.) from Desktop, Documents, or Downloads",
                "parameters": ["filename"]
            },
            
            # Media tools
            "play_song_on_spotify": {
                "function": media.spotify.play_song_on_spotify,
                "description": "Search and play a song on Spotify",
                "parameters": ["song_name"]
            },
            "spotify_play_pause": {
                "function": media.spotify.spotify_play_pause,
                "description": "Toggle play/pause on Spotify",
                "parameters": []
            },
            "spotify_next": {
                "function": media.spotify.spotify_next,
                "description": "Skip to next track on Spotify",
                "parameters": []
            },
            "spotify_previous": {
                "function": media.spotify.spotify_previous,
                "description": "Go to previous track on Spotify",
                "parameters": []
            },
            
            # Routines
            "execute_routine": {
                "function": self._execute_routine_wrapper,
                "description": "Execute a predefined routine (morning, focus, end_of_day, meeting_prep)",
                "parameters": ["name"]
            },
            "list_routines": {
                "function": self._list_routines_wrapper,
                "description": "List all available routines",
                "parameters": []
            }
        }
    
    def get_tools_description(self) -> str:
        """Generate a description of all available tools for the LLM."""
        tools_desc = []
        for name, info in self.tools_registry.items():
            params = ", ".join(info["parameters"]) if info["parameters"] else "no parameters"
            tools_desc.append(f"- {name}: {info['description']} | params: {params}")
        return "\n".join(tools_desc)
    
    def orchestrate(self, user_input: str) -> Dict[str, Any]:
        """
        Main orchestration method. Analyzes user input and executes appropriate tools.
        If no tool exists, attempts to generate one using the code generator.
        
        Args:
            user_input: Natural language command from user
            
        Returns:
            Execution result with tool calls and responses
        """
        if not self.client:
            return {
                'success': False,
                'message': 'Orchestrator offline (no Groq API key)'
            }
        
        # Create system prompt with available tools
        tools_desc = self.get_tools_description()
        
        system_prompt = f"""You are SAGE, a desktop assistant. Analyze the user request and decide which tools to call.

Available tools:
{tools_desc}

Respond with JSON only in this exact format:
{{
    "thinking": "brief reasoning about what the user wants",
    "tool_calls": [
        {{"tool": "tool_name", "params": {{"param1": "value1", "param2": "value2"}}}}
    ],
    "response": "optional message to user if no tools needed or additional context",
    "needs_automation": false
}}

Rules:
1. If multiple tools are needed, include them all in tool_calls array
2. Use exact tool names from the list above
3. For GENERAL QUESTIONS (what is, explain, tell me about), provide direct answer in "response" field, do NOT use search_web
4. Only use search_web if user explicitly asks to "search" or "look up" something
5. If no tool matches but task could be automated with mouse/keyboard, set "needs_automation": true
6. Always include "thinking" field with your reasoning

Examples:
User: "open chrome and set volume to 50"
{{
    "thinking": "User wants to open Chrome browser and adjust system volume to 50%",
    "tool_calls": [
        {{"tool": "open_app", "params": {{"app_name": "chrome"}}}},
        {{"tool": "set_volume", "params": {{"level": 50}}}}
    ]
}}

User: "what is quantum computing"
{{
    "thinking": "User wants an explanation of quantum computing - this is a general knowledge question",
    "tool_calls": [],
    "response": "Quantum computing uses quantum mechanical phenomena like superposition and entanglement to process information in ways that classical computers cannot, potentially solving certain problems exponentially faster."
}}

User: "search for quantum computing news"
{{
    "thinking": "User explicitly wants to search for information online",
    "tool_calls": [
        {{"tool": "search_web", "params": {{"query": "quantum computing news"}}}}
    ]
}}

User: "create a birthday invitation document and open it in word"
{{
    "thinking": "User wants to create content and type it in Word - need to generate content, open Word, then type it",
    "tool_calls": [
        {{"tool": "generate_content", "params": {{"topic": "birthday invitation", "content_type": "invitation", "style": "friendly"}}}},
        {{"tool": "open_app", "params": {{"app_name": "word"}}}},
        {{"tool": "type_text", "params": {{"text": "$CONTENT_FROM_PREVIOUS_STEP", "press_enter": false}}}}
    ],
    "response": "I'll generate the invitation, open Word, and type it for you."
}}

User: "send birthday invitation to sujal of Parth on 15/12/2025 at 6 pm"
{{
    "thinking": "User wants to send a birthday invitation via WhatsApp - generate SHORT message then send",
    "tool_calls": [
        {{"tool": "generate_content", "params": {{"topic": "Birthday invitation for Parth's birthday party on 15th December 2025 at 6 PM", "content_type": "whatsapp", "style": "friendly"}}}},
        {{"tool": "send_whatsapp", "params": {{"contact_name": "Sujal", "message": "$CONTENT_FROM_PREVIOUS_STEP"}}}}
    ],
    "response": "I'll create a short birthday invitation and send it to Sujal on WhatsApp."
}}

User: "send whatsapp message to sujal about my birthday"
{{
    "thinking": "User wants to send a WhatsApp message about their birthday - generate SHORT casual message then send",
    "tool_calls": [
        {{"tool": "generate_content", "params": {{"topic": "Inviting friend to my birthday celebration", "content_type": "whatsapp", "style": "casual"}}}},
        {{"tool": "send_whatsapp", "params": {{"contact_name": "Sujal", "message": "$CONTENT_FROM_PREVIOUS_STEP"}}}}
    ],
    "response": "I'll send a birthday invitation message to Sujal on WhatsApp."
}}

User: "type hello world"
{{
    "thinking": "User wants to type text into the current window",
    "tool_calls": [
        {{"tool": "type_on_screen", "params": {{"text": "hello world", "typing_speed": "normal", "press_enter": false}}}}
    ]
}}

User: "type this text slowly: Welcome to SAGE"
{{
    "thinking": "User wants to type text slowly on screen",
    "tool_calls": [
        {{"tool": "type_on_screen", "params": {{"text": "Welcome to SAGE", "typing_speed": "slow", "press_enter": false}}}}
    ]
}}

User: "clear and type new message"
{{
    "thinking": "User wants to clear current content and type new text",
    "tool_calls": [
        {{"tool": "clear_and_type", "params": {{"text": "new message", "clear_method": "select_all"}}}}
    ]
}}

User: "type in uppercase: hello world"
{{
    "thinking": "User wants to type text in uppercase format",
    "tool_calls": [
        {{"tool": "type_formatted_text", "params": {{"text": "hello world", "format_type": "uppercase"}}}}
    ]
}}

User: "play Shape of You on spotify"
{{
    "thinking": "User wants to play a specific song on Spotify - use the dedicated Spotify tool",
    "tool_calls": [
        {{"tool": "play_song_on_spotify", "params": {{"song_name": "Shape of You"}}}}
    ],
    "response": "Playing Shape of You on Spotify."
}}

User: "next song" or "skip track"
{{
    "thinking": "User wants to skip to next track",
    "tool_calls": [
        {{"tool": "spotify_next", "params": {{}}}}
    ],
    "response": "Skipping to next track."
}}

User: "pause music" or "play music"
{{
    "thinking": "User wants to toggle play/pause",
    "tool_calls": [
        {{"tool": "spotify_play_pause", "params": {{}}}}
    ],
    "response": "Toggled play/pause."
}}

User: "schedule a meeting with sujal"
{{
    "thinking": "User wants to schedule a meeting but didn't provide date/time - need to ask",
    "tool_calls": [
        {{"tool": "schedule_meeting", "params": {{"attendee": "sujal"}}}}
    ]
}}

User: "schedule a meeting with manager tomorrow at 3 pm"
{{
    "thinking": "User wants to schedule a meeting with all details provided",
    "tool_calls": [
        {{"tool": "schedule_meeting", "params": {{"attendee": "manager", "date": "tomorrow", "time": "3 pm"}}}}
    ],
    "response": "Scheduling a meeting with your manager for tomorrow at 3 PM."
}}

User: "start a quick meeting with john"
{{
    "thinking": "User wants to start an immediate Google Meet",
    "tool_calls": [
        {{"tool": "quick_meeting", "params": {{"attendee": "john"}}}}
    ],
    "response": "Starting a Google Meet. You can invite John once it opens."
}}

User: "call sujal on whatsapp"
{{
    "thinking": "User wants to make a WhatsApp voice call",
    "tool_calls": [
        {{"tool": "whatsapp_call", "params": {{"contact_name": "Sujal"}}}}
    ],
    "response": "Calling Sujal on WhatsApp."
}}

User: "video call mom on whatsapp"
{{
    "thinking": "User wants to make a WhatsApp video call",
    "tool_calls": [
        {{"tool": "whatsapp_video_call", "params": {{"contact_name": "Mom"}}}}
    ],
    "response": "Starting video call with Mom on WhatsApp."
}}

User: "what's on my screen" or "what do you see"
{{
    "thinking": "User wants to know what's currently displayed on their screen",
    "tool_calls": [
        {{"tool": "whats_on_screen", "params": {{}}}}
    ],
    "response": "Let me analyze your screen."
}}

User: "what options are available" or "what can I click"
{{
    "thinking": "User wants to know what buttons/options are visible",
    "tool_calls": [
        {{"tool": "get_screen_options", "params": {{}}}}
    ],
    "response": "Let me check what options are available on your screen."
}}

User: "where is the save button"
{{
    "thinking": "User wants to find a specific element on screen",
    "tool_calls": [
        {{"tool": "analyze_screen", "params": {{"question": "Where is the save button located?"}}}}
    ],
    "response": "Let me find the save button for you."
}}

User: "analyze document resume" or "analyze my thesis"
{{
    "thinking": "User wants to analyze a document file",
    "tool_calls": [
        {{"tool": "analyze_document", "params": {{"filename": "resume"}}}}
    ],
    "response": "I'll find and analyze the document for you."
}}

User: "analyze the report file"
{{
    "thinking": "User wants to analyze a report document",
    "tool_calls": [
        {{"tool": "analyze_document", "params": {{"filename": "report"}}}}
    ],
    "response": "Finding and analyzing the report file."
}}

User: "find my resume file" or "search for resume.pdf"
{{
    "thinking": "User wants to search for a specific file on their system",
    "tool_calls": [
        {{"tool": "search_file", "params": {{"filename": "resume"}}}}
    ],
    "response": "Searching for your resume file."
}}

User: "find all my documents" or "search for document files"
{{
    "thinking": "User wants to find files by type - documents",
    "tool_calls": [
        {{"tool": "search_files_by_type", "params": {{"file_type": "document"}}}}
    ],
    "response": "Searching for document files."
}}

User: "find images in downloads folder"
{{
    "thinking": "User wants to search for image files in a specific location",
    "tool_calls": [
        {{"tool": "search_files_by_type", "params": {{"file_type": "image", "search_path": "C:\\Users\\Downloads"}}}}
    ],
    "response": "Searching for images in your downloads folder."
}}

User: "open location of config.txt"
{{
    "thinking": "User wants to open the folder containing a specific file",
    "tool_calls": [
        {{"tool": "search_file", "params": {{"filename": "config.txt"}}}},
        {{"tool": "open_file_location", "params": {{"filepath": "$CONTENT_FROM_PREVIOUS_STEP"}}}}
    ],
    "response": "Finding and opening the location of config.txt."
}}

User: "find in downloads" or "search downloads for [filename]"
{{
    "thinking": "User wants to search only in Downloads folder with GUI options",
    "tool_calls": [
        {{"tool": "search_downloads", "params": {{"filename": "filename"}}}}
    ],
    "response": "Searching Downloads folder and showing clickable options."
}}

User: "find setup file in downloads"
{{
    "thinking": "User wants to find setup files specifically in Downloads with GUI",
    "tool_calls": [
        {{"tool": "search_downloads", "params": {{"filename": "setup"}}}}
    ],
    "response": "Searching for setup files in Downloads with clickable options to open."
}}

User: "send email to manager"
{{
    "thinking": "User wants to send email but didn't specify subject or content - need to ask",
    "tool_calls": [],
    "response": "I can send an email to your manager. What should the email be about?"
}}

User: "send leave letter to manager about sick leave tomorrow"
{{
    "thinking": "User wants to send leave email - generate content and send via browser",
    "tool_calls": [
        {{"tool": "generate_content", "params": {{"topic": "sick leave request for tomorrow", "content_type": "letter", "style": "formal"}}}},
        {{"tool": "send_email_browser", "params": {{"recipient_name": "manager", "subject": "Sick Leave Request", "body": "$CONTENT_FROM_PREVIOUS_STEP"}}}}
    ],
    "response": "I'll compose a sick leave letter and send it to your manager."
}}

User: "send resignation email to hr"
{{
    "thinking": "User wants to send resignation email to HR - generate formal resignation letter and send via browser",
    "tool_calls": [
        {{"tool": "generate_content", "params": {{"topic": "resignation letter", "content_type": "letter", "style": "formal"}}}},
        {{"tool": "send_email_browser", "params": {{"recipient_name": "hr", "subject": "Resignation Notice", "body": "$CONTENT_FROM_PREVIOUS_STEP"}}}}
    ],
    "response": "I'll compose a resignation letter and send it to HR."
}}

User: "email sujal about the meeting"
{{
    "thinking": "User wants to email sujal - use recipient_name to look up contact",
    "tool_calls": [
        {{"tool": "send_email_browser", "params": {{"recipient_name": "sujal", "subject": "Meeting", "body": ""}}}}
    ],
    "response": "I'll compose an email to Sujal about the meeting."
}}

User: "click the save button in notepad"
{{
    "thinking": "User wants to click a specific button in an application - this needs GUI automation",
    "tool_calls": [],
    "needs_automation": true,
    "response": "I can create an automation tool to click the save button in Notepad."
}}"""

        try:
            # Call Groq with JSON mode
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                response_format={"type": "json_object"},
                temperature=0.1  # Low temperature for consistent tool calling
            )
            
            # Parse the JSON response
            content = response.choices[0].message.content
            parsed = json.loads(content)
            
            # Check if we need to generate a new tool
            if parsed.get('needs_automation', False) and not parsed.get('tool_calls'):
                return self._handle_automation_request(user_input, parsed)
            
            # Execute the tool calls
            return self._execute_plan(parsed, user_input)
            
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'message': f'Failed to parse orchestrator response: {str(e)}',
                'raw_response': content if 'content' in locals() else 'No response'
            }
        except Exception as e:
            error_str = str(e)
            
            # Handle rate limit errors specifically
            if "429" in error_str or "rate limit" in error_str.lower():
                return self._handle_rate_limit(user_input)
            
            return {
                'success': False,
                'message': f'Orchestrator error: {str(e)}'
            }
    
    def _handle_automation_request(self, user_input: str, parsed_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle requests that need new automation tools to be generated.
        
        Args:
            user_input: Original user request
            parsed_response: Parsed LLM response indicating automation needed
            
        Returns:
            Result of tool generation and execution
        """
        from .code_generator import get_code_generator
        
        code_gen = get_code_generator()
        
        # Check if we can generate a tool for this
        if not code_gen.can_generate_tool(user_input):
            return {
                'success': False,
                'message': "I can't automate this task. It doesn't seem to involve GUI interactions.",
                'thinking': parsed_response.get('thinking', ''),
                'response': parsed_response.get('response', '')
            }
        
        # Generate the tool
        print(f"🔨 Generating automation tool for: {user_input}")
        gen_result = code_gen.generate_tool(user_input)
        
        if not gen_result['success']:
            return {
                'success': False,
                'message': f"Failed to generate automation tool: {gen_result['message']}",
                'thinking': parsed_response.get('thinking', ''),
                'generation_details': gen_result
            }
        
        # If the tool requires approval (dangerous operations), return for user confirmation
        if gen_result.get('requires_approval', False):
            return {
                'success': False,
                'message': gen_result['message'],
                'requires_approval': True,
                'generated_code': gen_result.get('code', ''),
                'thinking': parsed_response.get('thinking', '')
            }
        
        # Execute the newly generated tool
        function_name = gen_result['function_name']
        print(f"🚀 Executing generated tool: {function_name}")
        
        exec_result = code_gen.execute_generated_tool(function_name)
        
        return {
            'success': exec_result['success'],
            'message': f"Generated and executed tool '{function_name}': {exec_result['message']}",
            'thinking': parsed_response.get('thinking', ''),
            'generated_tool': {
                'name': function_name,
                'file_path': gen_result.get('file_path', ''),
                'reused': gen_result.get('reused', False)
            },
            'execution_result': exec_result,
            'type': 'generated_automation'
        }
    
    def _execute_plan(self, plan: Dict[str, Any], original_input: str) -> Dict[str, Any]:
        """
        Execute the planned tool calls with progress feedback.
        
        Args:
            plan: Parsed JSON plan from LLM
            original_input: Original user input for context
            
        Returns:
            Execution results
        """
        results = {
            'success': True,
            'original_input': original_input,
            'thinking': plan.get('thinking', ''),
            'tool_calls': [],
            'response': plan.get('response', ''),
            'execution_log': [],
            'progress_steps': []  # For GUI display
        }
        
        # If no tool calls, just return the response
        if not plan.get('tool_calls'):
            # Speak the response if it's a conversation
            if plan.get('response'):
                self._speak_response(plan['response'])
            return results
        
        # Announce start of execution
        num_tools = len(plan['tool_calls'])
        if num_tools > 1:
            start_msg = f"Executing {num_tools} tasks"
            self._speak_response(start_msg, priority=False)
            self._add_progress_step(results, "Starting execution", f"{num_tools} tasks planned")
        elif num_tools == 1:
            # Announce single task with friendly name
            tool_name = plan['tool_calls'][0].get('tool')
            friendly_name = self._get_friendly_tool_name(tool_name)
            self._speak_response(friendly_name, priority=False)
        
        # Memory for passing data between steps
        step_memory = {}
        
        # Execute each tool call
        for i, tool_call in enumerate(plan['tool_calls']):
            tool_name = tool_call.get('tool')
            params = tool_call.get('params', {})
            
            # Resolve any variable references in params (e.g., $CONTENT_FROM_PREVIOUS_STEP)
            params = self._resolve_params(params, step_memory)
            
            # Add progress step
            step_msg = f"Step {i+1}: {self._get_friendly_tool_name(tool_name)}"
            self._add_progress_step(results, step_msg, f"Executing {tool_name}")
            
            # Validate tool exists
            if tool_name not in self.tools_registry:
                error_msg = f"Unknown tool: {tool_name}"
                results['execution_log'].append({
                    'step': i + 1,
                    'tool': tool_name,
                    'status': 'error',
                    'error': error_msg
                })
                self._add_progress_step(results, f"❌ Step {i+1} failed", error_msg)
                results['success'] = False
                continue
            
            # Execute the tool
            try:
                tool_info = self.tools_registry[tool_name]
                tool_function = tool_info['function']
                
                # Log params before and after resolution
                print(f"🔧 Executing: {tool_name}")
                print(f"   Raw params: {tool_call.get('params', {})}")
                print(f"   Resolved params: {params}")
                if 'body' in params:
                    body_preview = params['body'][:100] + '...' if len(str(params.get('body', ''))) > 100 else params.get('body', '')
                    print(f"   Body preview: {body_preview}")
                
                # Call the tool function
                result = tool_function(**params)
                
                # Store result in memory for next steps
                if isinstance(result, dict):
                    if 'content' in result:
                        step_memory['CONTENT_FROM_PREVIOUS_STEP'] = result['content']
                        step_memory['LAST_CONTENT'] = result['content']
                        print(f"   📝 Stored content in memory ({len(result['content'])} chars)")
                    if 'result' in result:
                        step_memory['LAST_RESULT'] = result['result']
                    if 'message' in result:
                        step_memory['LAST_MESSAGE'] = result['message']
                
                # Log the execution
                results['tool_calls'].append({
                    'tool': tool_name,
                    'params': params,
                    'result': result
                })
                
                results['execution_log'].append({
                    'step': i + 1,
                    'tool': tool_name,
                    'status': 'success',
                    'result': str(result)[:100] + '...' if len(str(result)) > 100 else str(result)
                })
                
                # Add success progress step
                success_msg = self._get_success_message(tool_name, result)
                self._add_progress_step(results, f"✅ Step {i+1} completed", success_msg)
                
            except Exception as e:
                error_msg = f"Error executing {tool_name}: {str(e)}"
                results['execution_log'].append({
                    'step': i + 1,
                    'tool': tool_name,
                    'status': 'error',
                    'error': error_msg
                })
                self._add_progress_step(results, f"❌ Step {i+1} failed", error_msg)
                results['success'] = False
        
        # Announce completion
        successful_steps = len([log for log in results['execution_log'] if log['status'] == 'success'])
        failed_steps = len([log for log in results['execution_log'] if log['status'] == 'error'])
        
        if failed_steps == 0:
            completion_msg = f"All {successful_steps} tasks completed successfully"
        else:
            completion_msg = f"Completed with {successful_steps} successful and {failed_steps} failed tasks"
        
        self._speak_response(completion_msg, priority=False)
        self._add_progress_step(results, "🎉 Execution finished", completion_msg)
        
        return results
    
    def _get_friendly_tool_name(self, tool_name: str) -> str:
        """Convert tool name to friendly description."""
        friendly_names = {
            'open_app': 'Opening application',
            'close_app': 'Closing application', 
            'set_volume': 'Setting volume',
            'set_brightness': 'Setting brightness',
            'search_web': 'Searching web',
            'send_whatsapp': 'Sending WhatsApp message',
            'send_email_browser': 'Composing email',
            'calculate': 'Calculating',
            'get_weather': 'Getting weather',
            'get_time': 'Getting current time',
            'get_date': 'Getting current date',
            'execute_routine': 'Running routine',
            'mute': 'Muting audio',
            'unmute': 'Unmuting audio',
            'find_contact': 'Looking up contact',
            'smart_email_lookup': 'Preparing email'
        }
        return friendly_names.get(tool_name, tool_name.replace('_', ' ').title())
    
    def _get_success_message(self, tool_name: str, result: Dict[str, Any]) -> str:
        """Extract meaningful success message from tool result."""
        if isinstance(result, dict):
            if result.get('message'):
                return result['message']
            elif result.get('response'):
                return result['response']
            elif result.get('result'):
                return str(result['result'])
        return "Task completed"
    
    def _resolve_params(self, params: Dict[str, Any], memory: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve variable references in parameters.
        Variables look like $VARIABLE_NAME.
        """
        resolved = {}
        for key, value in params.items():
            if isinstance(value, str) and value.startswith('$'):
                var_name = value[1:]  # Remove $
                if var_name in memory:
                    resolved[key] = memory[var_name]
                else:
                    resolved[key] = value  # Keep original if not found
            else:
                resolved[key] = value
        return resolved
    
    def _add_progress_step(self, results: Dict[str, Any], title: str, description: str):
        """Add a progress step for GUI display."""
        results['progress_steps'].append({
            'title': title,
            'description': description,
            'timestamp': time.time()
        })
    
    def _speak_response(self, text: str, priority: bool = True):
        """Speak a response using TTS."""
        try:
            from voice.tts import speak
            speak(text, priority=priority)
        except ImportError:
            # TTS not available, skip
            pass
        except Exception as e:
            print(f"TTS error: {e}")
    
    def _handle_rate_limit(self, user_input: str) -> Dict[str, Any]:
        """
        Handle rate limit errors with fallback mechanisms.
        
        Args:
            user_input: Original user request
            
        Returns:
            Fallback response or rate limit message
        """
        # Try simple pattern matching for common commands
        user_lower = user_input.lower()
        
        # System commands
        if "open" in user_lower and any(app in user_lower for app in ["chrome", "notepad", "calculator", "spotify"]):
            app_name = None
            for app in ["chrome", "notepad", "calculator", "spotify", "word", "excel"]:
                if app in user_lower:
                    app_name = app
                    break
            
            if app_name:
                from tools.system.app_launcher import open_app
                result = open_app(app_name)
                return {
                    'success': result.get('success', False),
                    'message': result.get('message', f'Attempted to open {app_name}'),
                    'response': f'Opened {app_name}' if result.get('success') else f'Failed to open {app_name}',
                    'fallback': True
                }
        
        # Volume commands
        if "volume" in user_lower:
            import re
            volume_match = re.search(r'(\d+)', user_input)
            if volume_match:
                level = int(volume_match.group(1))
                from tools.system.volume import set_volume
                result = set_volume(level)
                return {
                    'success': result.get('success', False),
                    'message': result.get('message', f'Set volume to {level}'),
                    'response': f'Volume set to {level}%',
                    'fallback': True
                }
        
        # Time commands
        if any(word in user_lower for word in ["time", "clock"]):
            from tools.productivity.datetime_tool import get_time
            result = get_time()
            return {
                'success': True,
                'message': result.get('result', 'Time retrieved'),
                'response': f"The current time is {result.get('result', 'unknown')}",
                'fallback': True
            }
        
        # Weather commands
        if "weather" in user_lower:
            # Extract city if mentioned
            cities = ["mumbai", "delhi", "bangalore", "chennai", "kolkata", "pune", "hyderabad"]
            city = "mumbai"  # default
            for c in cities:
                if c in user_lower:
                    city = c
                    break
            
            from tools.productivity.weather import get_weather
            result = get_weather(city)
            return {
                'success': result.get('success', False),
                'message': result.get('message', f'Weather for {city}'),
                'response': result.get('message', f'Weather information for {city}'),
                'fallback': True
            }
        
        # Calculator commands
        if any(word in user_lower for word in ["calculate", "math", "plus", "minus", "times", "multiply", "divide"]):
            # Simple math extraction
            import re
            math_pattern = r'(\d+)\s*(?:plus|\+|times|\*|x|minus|-|divided by|/)\s*(\d+)'
            match = re.search(math_pattern, user_lower)
            if match:
                num1, num2 = int(match.group(1)), int(match.group(2))
                if "plus" in user_lower or "+" in user_lower:
                    result = num1 + num2
                    operation = f"{num1} + {num2}"
                elif "times" in user_lower or "*" in user_lower or "x" in user_lower:
                    result = num1 * num2
                    operation = f"{num1} × {num2}"
                elif "minus" in user_lower or "-" in user_lower:
                    result = num1 - num2
                    operation = f"{num1} - {num2}"
                elif "divided" in user_lower or "/" in user_lower:
                    result = num1 / num2 if num2 != 0 else "undefined"
                    operation = f"{num1} ÷ {num2}"
                
                return {
                    'success': True,
                    'message': f'{operation} = {result}',
                    'response': f'{operation} equals {result}',
                    'fallback': True
                }
        
        # Downloads search commands
        if "downloads" in user_lower and any(word in user_lower for word in ["find", "search", "locate"]):
            # Extract filename from downloads search patterns
            import re
            
            filename = None
            if "find" in user_lower and "downloads" in user_lower:
                # "find setup in downloads" -> "setup"
                match = re.search(r'find (.+?) in downloads', user_lower)
                if match:
                    filename = match.group(1).strip()
                else:
                    # "find in downloads" -> ask for filename
                    return {
                        'success': False,
                        'message': 'What file do you want to find in Downloads?',
                        'response': 'What file are you looking for in your Downloads folder?',
                        'fallback': True
                    }
            elif "search downloads" in user_lower:
                # "search downloads for setup" -> "setup"
                match = re.search(r'search downloads for (.+?)$', user_lower)
                if match:
                    filename = match.group(1).strip()
            
            if filename:
                from tools.system.downloads_search import search_downloads
                result = search_downloads(filename)
                
                if result.get('success'):
                    response = result.get('message', f"Found files in Downloads matching '{filename}'")
                    if result.get('gui_shown'):
                        response += " - Click to open from the popup window."
                else:
                    response = result.get('message', f"No files found in Downloads matching '{filename}'")
                
                return {
                    'success': result.get('success', False),
                    'message': result.get('message', response),
                    'response': response,
                    'fallback': True
                }
        
        # General file search commands
        elif any(word in user_lower for word in ["find", "search", "locate"]) and any(word in user_lower for word in ["file", "document", "folder"]):
            # Extract filename from common patterns
            import re
            
            # Try to extract filename
            filename = None
            if "find" in user_lower:
                # "find my resume" -> "resume"
                match = re.search(r'find (?:my )?(.+?)(?:\s+file)?$', user_lower)
                if match:
                    filename = match.group(1).strip()
            elif "search for" in user_lower:
                # "search for config.txt" -> "config.txt"
                match = re.search(r'search for (.+?)(?:\s+file)?$', user_lower)
                if match:
                    filename = match.group(1).strip()
            
            if filename:
                from tools.system.file_search import search_file
                result = search_file(filename, max_results=5)
                
                if result.get('success') and result.get('results'):
                    files_found = result['results']
                    response = f"Found {len(files_found)} file(s) matching '{filename}':\n"
                    for i, file_info in enumerate(files_found[:3], 1):
                        response += f"{i}. {file_info['name']} in {file_info['directory']}\n"
                    if len(files_found) > 3:
                        response += f"... and {len(files_found) - 3} more"
                else:
                    response = f"No files found matching '{filename}'"
                
                return {
                    'success': result.get('success', False),
                    'message': result.get('message', response),
                    'response': response,
                    'fallback': True
                }
        
        # Text typing commands
        if "type" in user_lower and not any(word in user_lower for word in ["file", "document"]):
            # Extract text to type
            import re
            
            text_to_type = None
            typing_speed = "normal"
            
            if "type " in user_lower:
                # "type hello world" -> "hello world"
                match = re.search(r'type (.+?)$', user_lower)
                if match:
                    text_to_type = match.group(1).strip()
                    
                    # Check for speed modifiers
                    if "slowly" in text_to_type or "slow" in text_to_type:
                        typing_speed = "slow"
                        text_to_type = re.sub(r'\b(slowly|slow)\b:?\s*', '', text_to_type).strip()
                    elif "fast" in text_to_type or "quickly" in text_to_type:
                        typing_speed = "fast"
                        text_to_type = re.sub(r'\b(fast|quickly)\b:?\s*', '', text_to_type).strip()
            
            if text_to_type:
                from tools.system.text_typer import type_on_screen
                result = type_on_screen(text_to_type, typing_speed=typing_speed)
                
                if result.get('success'):
                    response = f"Typed '{text_to_type}' at {typing_speed} speed"
                else:
                    response = result.get('message', f"Failed to type '{text_to_type}'")
                
                return {
                    'success': result.get('success', False),
                    'message': result.get('message', response),
                    'response': response,
                    'fallback': True
                }
        
        # Document analysis commands
        if any(word in user_lower for word in ["analyze", "analysis"]) and any(word in user_lower for word in ["document", "file", "pdf", "report", "paper"]):
            # Extract document name
            import re
            
            document_name = None
            if "analyze document" in user_lower:
                match = re.search(r'analyze document (.+?)$', user_lower)
                if match:
                    document_name = match.group(1).strip()
            elif "analyze" in user_lower and ("file" in user_lower or "pdf" in user_lower or "report" in user_lower or "paper" in user_lower):
                # "analyze my report" -> "report"
                match = re.search(r'analyze (?:my |the )?(.+?)$', user_lower)
                if match:
                    document_name = match.group(1).strip()
            
            if document_name:
                from tools.ai.file_analyzer import analyze_document
                result = analyze_document(document_name)
                
                if result.get('success'):
                    analysis = result.get('analysis', 'Analysis completed')
                    # Truncate analysis for rate limit response
                    if len(analysis) > 300:
                        analysis = analysis[:297] + "..."
                    import os
                    response = f"Document '{os.path.basename(result.get('file_path', document_name))}' analysis:\n{analysis}"
                else:
                    response = result.get('message', f"Could not analyze document '{document_name}'")
                
                return {
                    'success': result.get('success', False),
                    'message': result.get('message', response),
                    'response': response,
                    'fallback': True
                }
        
        # Default rate limit message
        return {
            'success': False,
            'message': 'Rate limit reached. Please wait a moment and try again.',
            'response': 'I\'m currently experiencing high usage. Please wait a moment and try your command again. You can also try simpler commands like "open chrome" or "what time is it".',
            'rate_limited': True,
            'retry_after': 60  # Suggest waiting 60 seconds
        }
    
    def _execute_routine_wrapper(self, name: str) -> Dict[str, Any]:
        """Wrapper for routine execution."""
        from routines.routine_manager import execute_routine
        return execute_routine(name)
    
    def _list_routines_wrapper(self) -> Dict[str, Any]:
        """Wrapper for listing routines."""
        from routines.routine_manager import list_routines
        return list_routines()
    
    def chat(self, user_input: str) -> str:
        """
        Simple chat mode without tool calling.
        For when user just wants to talk.
        """
        if not self.client:
            return "I'm offline (no API key)"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are SAGE, a helpful desktop assistant. Be concise and friendly."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate limit" in error_str.lower():
                return "I'm currently experiencing high usage. Please wait a moment and try again. You can ask me simple questions or try basic commands like 'open chrome' or 'what time is it'."
            return f"I'm having trouble right now: {str(e)}"


# Global instance
_orchestrator = None

def get_orchestrator() -> OrchestratorAgent:
    """Get or create the global orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = OrchestratorAgent()
    return _orchestrator