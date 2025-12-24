"""
Particle Animation UI
Modern UI with Thinking/Processing section like ChatGPT/Gemini.
Shows workflow in collapsible thinking section, final output in main chat.
"""

import tkinter as tk
from tkinter import font
import sys
import threading
import queue
import math
import random
import time
from core.task_executor import get_executor
from voice import listen, speak

class Particle:
    def __init__(self, canvas, x, y, size, color):
        self.canvas = canvas
        self.id = self.canvas.create_oval(x-size, y-size, x+size, y+size, fill=color, outline="")
        self.size = size
        self.x = x; self.y = y
    def move(self, x, y):
        self.canvas.coords(self.id, x - self.size, y - self.size, x + self.size, y + self.size)
        self.x = x; self.y = y

class ParticleWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("SAGE Particle UI")
        self.geometry("500x820+100+100")
        self.overrideredirect(True)
        self.config(bg='#121212')
        self.attributes("-topmost", True)
        
        # Draggable
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.do_move)
        
        # Close Button
        self.close_btn = tk.Button(self, text="X", command=self.destroy, bg="#1e1e1e", fg="white", relief="flat")
        self.close_btn.place(x=470, y=10)
        
        # Title
        tk.Label(self, text="SAGE AI ASSISTANT", fg="#e0e0e0", bg="#121212", font=("Roboto Medium", 14)).pack(pady=15)
        
        # Animation Canvas (smaller)
        self.animation_canvas = tk.Canvas(self, bg="#121212", highlightthickness=0, height=200)
        self.animation_canvas.pack(fill="x", pady=10)
        
        self.particles = []
        self.center_x = 250
        self.center_y = 100
        self.angle_step = 0
        self._create_particles()
        
        # ========== THINKING/PROCESSING SECTION (Collapsible) ==========
        self.thinking_frame = tk.Frame(self, bg="#1a1a1a", relief="flat")
        self.thinking_frame.pack(fill="x", padx=15, pady=(5, 0))
        
        # Thinking header (clickable to expand/collapse)
        self.thinking_header = tk.Frame(self.thinking_frame, bg="#1a1a1a")
        self.thinking_header.pack(fill="x")
        
        self.thinking_toggle_btn = tk.Label(
            self.thinking_header, 
            text="▶ Thinking...", 
            fg="#666666", 
            bg="#1a1a1a", 
            font=("Roboto", 9),
            cursor="hand2"
        )
        self.thinking_toggle_btn.pack(side="left", padx=5, pady=3)
        self.thinking_toggle_btn.bind("<Button-1>", self._toggle_thinking)
        
        # Thinking content (hidden by default)
        self.thinking_content = tk.Text(
            self.thinking_frame, 
            bg="#1a1a1a", 
            fg="#555555", 
            height=4, 
            relief="flat", 
            font=("Consolas", 8),
            wrap="word"
        )
        self.thinking_content.pack(fill="x", padx=5, pady=(0, 5))
        self.thinking_content.pack_forget()  # Hidden initially
        self.thinking_expanded = False
        self.thinking_frame.pack_forget()  # Hide entire section initially
        
        # ========== MAIN CHAT OUTPUT ==========
        tk.Label(self, text="💬 Chat", fg="#888888", bg="#121212", font=("Roboto", 9)).pack(anchor="w", padx=20)
        
        self.text_area = tk.Text(
            self, 
            bg="#1e1e1e", 
            fg="#e0e0e0", 
            height=10, 
            relief="flat", 
            font=("Consolas", 10),
            wrap="word"
        )
        self.text_area.pack(fill="x", padx=15, pady=(5, 10))
        
        # Configure text tags for styling
        self.text_area.tag_configure("user", foreground="#00ff88")
        self.text_area.tag_configure("sage", foreground="#88ccff")
        self.text_area.tag_configure("system", foreground="#666666")
        
        # ========== MY TASKS SECTION (Recordings) ==========
        self.tasks_frame = tk.Frame(self, bg="#1a1a1a", relief="flat")
        self.tasks_frame.pack(fill="x", padx=15, pady=(5, 0))
        
        # Tasks header
        tasks_header = tk.Frame(self.tasks_frame, bg="#1a1a1a")
        tasks_header.pack(fill="x")
        
        tk.Label(tasks_header, text="📋 My Tasks", fg="#888888", bg="#1a1a1a", font=("Roboto", 9)).pack(side="left", padx=5, pady=3)
        
        # Record button
        self.record_btn = tk.Button(
            tasks_header,
            text="⏺ Record",
            command=self._start_recording,
            bg="#ff4444",
            fg="white",
            relief="flat",
            font=("Roboto", 8),
            cursor="hand2"
        )
        self.record_btn.pack(side="right", padx=5, pady=2)
        
        # Tasks list (scrollable)
        self.tasks_listbox = tk.Listbox(
            self.tasks_frame,
            bg="#1e1e1e",
            fg="#e0e0e0",
            height=4,
            relief="flat",
            font=("Consolas", 9),
            selectbackground="#333333",
            selectforeground="#00ff88"
        )
        self.tasks_listbox.pack(fill="x", padx=5, pady=5)
        self.tasks_listbox.bind("<Double-Button-1>", self._play_selected_task)
        
        # Refresh tasks list
        self._refresh_tasks()
        
        # ========== STATUS BAR ==========
        self.status_frame = tk.Frame(self, bg="#121212")
        self.status_frame.pack(fill="x", padx=15, pady=5)
        
        self.status_lbl = tk.Label(
            self.status_frame, 
            text="🟢 Ready", 
            fg="#666666", 
            bg="#121212",
            font=("Roboto", 10)
        )
        self.status_lbl.pack(side="left")
        
        # Stop button (to interrupt TTS and return to wake word listening)
        self.stop_btn = tk.Button(
            self.status_frame,
            text="⏹ Stop",
            command=self._stop_and_reset,
            bg="#ff6666",
            fg="white",
            relief="flat",
            font=("Roboto", 8),
            cursor="hand2"
        )
        self.stop_btn.pack(side="right", padx=5)
        
        # ========== TEXT INPUT SECTION ==========
        self.input_frame = tk.Frame(self, bg="#121212")
        self.input_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        # Input label
        tk.Label(
            self.input_frame, 
            text="💬 Say wake word or type your command:", 
            fg="#888888", 
            bg="#121212", 
            font=("Roboto", 9)
        ).pack(anchor="w", pady=(0, 5))
        
        # Input entry with placeholder
        self.input_entry = tk.Entry(
            self.input_frame,
            bg="#1e1e1e",
            fg="#e0e0e0",
            insertbackground="#00ff88",
            relief="flat",
            font=("Consolas", 11)
        )
        self.input_entry.pack(fill="x", side="left", expand=True, ipady=8)
        self.input_entry.insert(0, "Type a command here...")
        self.input_entry.config(fg="#666666")
        
        # Bind events for placeholder behavior
        self.input_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.input_entry.bind("<FocusOut>", self._on_entry_focus_out)
        self.input_entry.bind("<Return>", self._on_entry_submit)
        
        # Send button
        self.send_btn = tk.Button(
            self.input_frame,
            text="➤",
            command=self._submit_text_command,
            bg="#00ff88",
            fg="#121212",
            relief="flat",
            font=("Roboto", 12),
            cursor="hand2",
            width=3
        )
        self.send_btn.pack(side="right", padx=(5, 0), ipady=4)
        
        # Recording state
        self.is_recording = False
        self.recording_thread = None
        
        # Voice control state
        self.voice_interrupted = False
        self.current_tts_thread = None
        
        # Internal Logic
        self.executor = get_executor()
        self.q = queue.Queue()
        
        # Start Animation Loop
        self._update_animation()
        self._process_queue()
        
        # Start Listening Loop in Background
        threading.Thread(target=self._voice_loop, daemon=True).start()

    def _create_particles(self):
        for _ in range(60):
            color = f'#{random.randint(0,100):02x}{random.randint(100,255):02x}{random.randint(200,255):02x}'
            p = Particle(self.animation_canvas, self.center_x, self.center_y, random.uniform(1, 3), color)
            p.angle_offset = random.uniform(0, 2 * math.pi)
            p.radius_x = random.uniform(50, 100)
            p.radius_y = random.uniform(50, 100)
            p.speed = random.uniform(0.5, 2.0)
            self.particles.append(p)

    def _update_animation(self):
        self.angle_step += 0.02
        for p in self.particles:
            angle = self.angle_step * p.speed + p.angle_offset
            x = self.center_x + p.radius_x * math.sin(angle * 3)
            y = self.center_y + p.radius_y * math.cos(angle * 2)
            p.move(x, y)
        self.after(20, self._update_animation)
    
    def _toggle_thinking(self, event=None):
        """Toggle thinking section visibility."""
        if self.thinking_expanded:
            self.thinking_content.pack_forget()
            self.thinking_toggle_btn.config(text="▶ Thinking...")
            self.thinking_expanded = False
        else:
            self.thinking_content.pack(fill="x", padx=5, pady=(0, 5))
            self.thinking_toggle_btn.config(text="▼ Thinking...")
            self.thinking_expanded = True
    
    def show_thinking(self, text):
        """Show thinking section with content."""
        self.q.put(('thinking_show', text))
    
    def hide_thinking(self):
        """Hide thinking section."""
        self.q.put(('thinking_hide',))
    
    def add_thinking_step(self, step_text):
        """Add a step to thinking section."""
        self.q.put(('thinking_step', step_text))
    
    def log_user(self, text):
        """Log user message."""
        self.q.put(('log_user', text))
    
    def log_sage(self, text):
        """Log SAGE response."""
        self.q.put(('log_sage', text))
    
    def log_system(self, text):
        """Log system message."""
        self.q.put(('log_system', text))
    
    def set_status(self, text, color="#666666"):
        """Update status bar."""
        self.q.put(('status', text, color))
    
    def _extract_response(self, result):
        """Extract the best response from execution result."""
        # For generated automation tools
        if result.get('type') == 'generated_automation':
            exec_result = result.get('execution_result', {})
            if exec_result.get('message'):
                return exec_result['message']
            return result.get('message', 'Task completed')
        
        # For agentic responses, check tool results first
        if result.get('type') == 'agentic' and result.get('tool_calls'):
            for tc in result['tool_calls']:
                tool_result = tc.get('result', {})
                if isinstance(tool_result, dict):
                    if 'response' in tool_result:
                        return tool_result['response']
                    elif 'result' in tool_result and tc['tool'] in ['get_time', 'get_date']:
                        return f"The time is {tool_result['result']}"
                    elif 'message' in tool_result:
                        return tool_result['message']
        
        # For orchestrator results with tool_calls
        if result.get('tool_calls'):
            # Get the last tool's response
            last_tool = result['tool_calls'][-1]
            tool_result = last_tool.get('result', {})
            if isinstance(tool_result, dict):
                if 'response' in tool_result:
                    return tool_result['response']
                elif 'message' in tool_result:
                    return tool_result['message']
        
        # Standard response extraction
        if result.get('response'): 
            return result['response']
        elif result.get('message'): 
            return result['message']
        elif result.get('result'): 
            val = result['result']
            if isinstance(val, dict):
                if 'response' in val:
                    return val['response']
                elif 'message' in val:
                    return val['message']
                elif 'result' in val:
                    return str(val['result'])
            return str(val)
        
        return "Task completed"
        
    def _process_queue(self):
        try:
            while True:
                msg = self.q.get_nowait()
                
                if isinstance(msg, tuple):
                    msg_type = msg[0]
                    
                    if msg_type == 'log_user':
                        self.text_area.insert(tk.END, f"You: {msg[1]}\n", "user")
                        self.text_area.see(tk.END)
                    
                    elif msg_type == 'log_sage':
                        self.text_area.insert(tk.END, f"SAGE: {msg[1]}\n\n", "sage")
                        self.text_area.see(tk.END)
                    
                    elif msg_type == 'log_system':
                        self.text_area.insert(tk.END, f"{msg[1]}\n", "system")
                        self.text_area.see(tk.END)
                    
                    elif msg_type == 'thinking_show':
                        self.thinking_frame.pack(fill="x", padx=15, pady=(5, 0))
                        self.thinking_content.delete(1.0, tk.END)
                        self.thinking_content.insert(tk.END, msg[1])
                        self.thinking_toggle_btn.config(text="▶ Thinking...", fg="#888888")
                    
                    elif msg_type == 'thinking_step':
                        self.thinking_content.insert(tk.END, f"\n• {msg[1]}")
                        self.thinking_toggle_btn.config(text="▶ Processing...", fg="#00ffff")
                    
                    elif msg_type == 'thinking_hide':
                        self.thinking_frame.pack_forget()
                        self.thinking_content.delete(1.0, tk.END)
                        self.thinking_expanded = False
                    
                    elif msg_type == 'status':
                        self.status_lbl.config(text=msg[1], fg=msg[2] if len(msg) > 2 else "#666666")
                    
                    elif msg_type == 'update_record_btn':
                        self.record_btn.config(text=msg[1], bg=msg[2])
                    
                    elif msg_type == 'refresh_tasks':
                        self._refresh_tasks()
                    
        except queue.Empty: 
            pass
        self.after(100, self._process_queue)

    def _voice_loop(self):
        from voice.wake_word import get_detector
        from voice.tts import speak as tts_speak
        
        self.log_system("🎤 Voice initialized. Say wake word to start...")
        
        # Store context for follow-up questions
        self.pending_context = None
        
        def on_wake():
            # Check if interrupted before starting
            if self.voice_interrupted:
                return
                
            self.log_system(">>> WAKE DETECTED <<<")
            self.set_status("🎤 Listening...", "#00ff00")
            
            # Always respond with "Yes, I'm listening"
            tts_speak("Yes, I'm listening", priority=True)
            
            # Wait a moment for TTS to finish before listening
            if not self.voice_interrupted:
                time.sleep(0.5)
            
            # Check for interruption before listening
            if self.voice_interrupted:
                self.set_status("🟢 Ready", "#666666")
                return
            
            # Listen with timeout (3 sec to start, 8 sec max phrase)
            cmd = listen(timeout=3, phrase_time_limit=8)
            
            # Check for interruption after listening
            if self.voice_interrupted:
                self.set_status("🟢 Ready", "#666666")
                return
            
            if cmd:
                # Process command and handle follow-ups
                self._process_command(cmd, tts_speak)
            else:
                # No command detected (unless interrupted)
                if not self.voice_interrupted:
                    self.log_system("No command detected. Say wake word to try again.")
                    tts_speak("I didn't catch that. Say the wake word to try again.", priority=True)
            
            # Reset status (unless already reset by interruption)
            if not self.voice_interrupted:
                self.set_status("🟢 Ready", "#666666")

        try:
            get_detector().start_listening(callback=on_wake)
        except Exception as e:
            self.log_system(f"⚠️ Voice Error: {e}")
    
    def _process_command(self, cmd, tts_speak):
        """Process a command and handle follow-up questions."""
        self.log_user(cmd)
        self.set_status("🧠 Processing...", "#00ffff")
        
        # Check for interruption before processing
        if self.voice_interrupted:
            self.set_status("🟢 Ready", "#666666")
            return
        
        # Execute with progress tracking
        result = self.executor.execute(cmd)
        
        # Check for interruption after processing
        if self.voice_interrupted:
            self.set_status("🟢 Ready", "#666666")
            return
        
        # Show thinking section with AI reasoning
        thinking_text = result.get('thinking', '')
        if thinking_text and not self.voice_interrupted:
            self.show_thinking(f"🧠 {thinking_text}")
        
        # Show progress steps in thinking section (not main chat)
        if result.get('progress_steps') and not self.voice_interrupted:
            for step in result['progress_steps']:
                if self.voice_interrupted:
                    break
                self.add_thinking_step(step['title'])
                time.sleep(0.2)
        
        # Check if this is a needs_info response (follow-up question)
        needs_followup = self._check_needs_followup(result)
        
        # Extract final response
        final_response = self._extract_response(result)
        
        # Log only the final response in main chat
        if not self.voice_interrupted:
            self.log_sage(final_response)
        
        # ALWAYS speak the final response (unless interrupted)
        if final_response and not self.voice_interrupted:
            print(f"[TTS] Speaking: {final_response[:100]}...")  # Debug log
            tts_speak(final_response, priority=True)
            
            # Wait for TTS to finish speaking (estimate based on text length)
            words = len(final_response.split())
            wait_time = max(2, min(words / 2.5, 15))  # 2-15 seconds
            
            # Wait in small increments to allow interruption
            for _ in range(int(wait_time * 10)):  # Check every 0.1 seconds
                if self.voice_interrupted:
                    break
                time.sleep(0.1)
        else:
            print("[TTS] No response to speak or interrupted")
        
        # Hide thinking section after speaking (unless interrupted)
        if not self.voice_interrupted:
            self.hide_thinking()
        
        # If needs follow-up, wait for user's answer immediately (no wake word needed)
        if needs_followup and not self.voice_interrupted:
            self._handle_followup(result, tts_speak)
        else:
            # End with listening message (unless interrupted)
            if not self.voice_interrupted:
                time.sleep(1)
                if not self.voice_interrupted:
                    tts_speak("Listening for your next command", priority=False)
                    self.log_system("Listening for your next command...")
    
    def _check_needs_followup(self, result):
        """Check if the result requires a follow-up answer from user."""
        # Check direct needs_info flag
        if result.get('needs_info'):
            return True
        
        # Check in tool_calls results
        if result.get('tool_calls'):
            for tc in result['tool_calls']:
                tool_result = tc.get('result', {})
                if isinstance(tool_result, dict) and tool_result.get('needs_info'):
                    return True
        
        # Check response text for question patterns
        response = self._extract_response(result)
        if response:
            response_lower = response.lower()
            question_patterns = [
                'who should i send',
                'what is the email about',
                'what should the email say',
                'when would you like',
                'what time should',
                'please provide',
                'who would you like',
                'what would you like',
            ]
            for pattern in question_patterns:
                if pattern in response_lower:
                    return True
        
        return False
    
    def _handle_followup(self, original_result, tts_speak):
        """Handle follow-up question - wait for user's answer without wake word."""
        self.log_system("⏳ Waiting for your answer...")
        self.set_status("🎤 Waiting for answer...", "#ffaa00")
        
        # Wait a moment before listening
        time.sleep(0.5)
        
        if self.voice_interrupted:
            return
        
        # Listen for follow-up answer (longer timeout since user is thinking)
        followup_answer = listen(timeout=5, phrase_time_limit=15)
        
        if self.voice_interrupted:
            return
        
        if followup_answer:
            # Combine context with follow-up answer
            # Get the missing info type from original result
            missing_info = self._get_missing_info(original_result)
            
            # Build a complete command with the follow-up info
            original_cmd = original_result.get('original_input', '')
            
            # Create a combined command that includes the follow-up
            if missing_info == 'recipient':
                combined_cmd = f"{original_cmd} to {followup_answer}"
            elif missing_info == 'subject':
                combined_cmd = f"{original_cmd} about {followup_answer}"
            elif missing_info == 'body':
                combined_cmd = f"{original_cmd} saying {followup_answer}"
            elif missing_info == 'date':
                combined_cmd = f"{original_cmd} on {followup_answer}"
            elif missing_info == 'time':
                combined_cmd = f"{original_cmd} at {followup_answer}"
            elif missing_info == 'attendee':
                combined_cmd = f"{original_cmd} with {followup_answer}"
            else:
                # Generic combination
                combined_cmd = f"{original_cmd} {followup_answer}"
            
            self.log_system(f"📝 Combined: {combined_cmd}")
            
            # Process the combined command
            self._process_command(combined_cmd, tts_speak)
        else:
            # No follow-up answer received
            if not self.voice_interrupted:
                self.log_system("No answer received. Say wake word to try again.")
                tts_speak("I didn't hear your answer. Say the wake word to start over.", priority=True)
    
    def _get_missing_info(self, result):
        """Get the type of missing info from result."""
        # Check direct missing field
        if result.get('missing'):
            return result['missing']
        
        # Check in tool_calls results
        if result.get('tool_calls'):
            for tc in result['tool_calls']:
                tool_result = tc.get('result', {})
                if isinstance(tool_result, dict) and tool_result.get('missing'):
                    return tool_result['missing']
        
        return None
    
    def _stop_and_reset(self):
        """Stop current TTS and return to wake word listening state."""
        try:
            # Set interrupt flag
            self.voice_interrupted = True
            
            # Stop TTS immediately
            from voice.tts import stop_speech
            stop_speech()
            
            # Log the interruption
            self.log_system("🛑 Stopped - returning to wake word listening...")
            
            # Reset status
            self.set_status("🟢 Ready", "#666666")
            
            # Hide thinking section if visible
            self.hide_thinking()
            
            # Reset interrupt flag after a moment
            threading.Timer(1.0, lambda: setattr(self, 'voice_interrupted', False)).start()
            
        except Exception as e:
            self.log_system(f"⚠️ Stop Error: {e}")
    
    # ========== TEXT INPUT METHODS ==========
    def _on_entry_focus_in(self, event):
        """Handle focus in on text entry - clear placeholder."""
        if self.input_entry.get() == "Type a command here...":
            self.input_entry.delete(0, tk.END)
            self.input_entry.config(fg="#e0e0e0")
    
    def _on_entry_focus_out(self, event):
        """Handle focus out on text entry - restore placeholder if empty."""
        if not self.input_entry.get():
            self.input_entry.insert(0, "Type a command here...")
            self.input_entry.config(fg="#666666")
    
    def _on_entry_submit(self, event):
        """Handle Enter key press in text entry."""
        self._submit_text_command()
    
    def _submit_text_command(self):
        """Submit the text command for processing."""
        cmd = self.input_entry.get().strip()
        
        # Ignore placeholder text
        if not cmd or cmd == "Type a command here...":
            return
        
        # Clear the input
        self.input_entry.delete(0, tk.END)
        
        # Process in background thread
        threading.Thread(target=self._process_text_command, args=(cmd,), daemon=True).start()
    
    def _process_text_command(self, cmd):
        """Process a text command (same as voice but without TTS prompts)."""
        from voice.tts import speak as tts_speak
        
        self.log_user(cmd)
        self.set_status("🧠 Processing...", "#00ffff")
        
        # Execute with progress tracking
        result = self.executor.execute(cmd)
        
        # Show thinking section with AI reasoning
        thinking_text = result.get('thinking', '')
        if thinking_text:
            self.show_thinking(f"🧠 {thinking_text}")
        
        # Show progress steps in thinking section
        if result.get('progress_steps'):
            for step in result['progress_steps']:
                self.add_thinking_step(step['title'])
                time.sleep(0.2)
        
        # Extract final response
        final_response = self._extract_response(result)
        
        # Log the response
        self.log_sage(final_response)
        
        # Speak the response
        if final_response:
            tts_speak(final_response, priority=True)
        
        # Hide thinking section
        self.hide_thinking()
        
        # Reset status
        self.set_status("🟢 Ready", "#666666")

    # ========== RECORDING METHODS ==========
    def _refresh_tasks(self):
        """Refresh the tasks list from saved recordings."""
        self.tasks_listbox.delete(0, tk.END)
        try:
            from recorder.action_player import get_player
            player = get_player()
            recordings = player.list_recordings()
            for rec in recordings:
                self.tasks_listbox.insert(tk.END, f"▶ {rec}")
            if not recordings:
                self.tasks_listbox.insert(tk.END, "(No recordings yet)")
        except Exception as e:
            self.tasks_listbox.insert(tk.END, f"(Error: {e})")
    
    def _start_recording(self):
        """Start recording with countdown."""
        if self.is_recording:
            return
        
        # Ask for recording name
        from tkinter import simpledialog
        name = simpledialog.askstring("Record Task", "Enter a name for this recording:", parent=self)
        if not name:
            return
        
        # Clean name
        name = name.replace(" ", "_").replace("/", "_").replace("\\", "_")
        
        # Start countdown in separate thread
        threading.Thread(target=self._recording_countdown, args=(name,), daemon=True).start()
    
    def _recording_countdown(self, name):
        """Show countdown before recording starts."""
        from voice.tts import speak as tts_speak
        from recorder.action_recorder import get_recorder
        from pynput import keyboard
        
        # Countdown
        for i in range(3, 0, -1):
            self.log_system(f"Recording starts in {i}...")
            tts_speak(str(i), priority=True)
            time.sleep(1)
        
        self.log_system("🔴 RECORDING! Press ESC to stop.")
        tts_speak("Recording started. Press Escape to stop.", priority=True)
        self.set_status("🔴 Recording...", "#ff0000")
        self.is_recording = True
        
        # Update button
        self.q.put(('update_record_btn', '⏹ Stop', '#00ff00'))
        
        # Start recorder
        recorder = get_recorder()
        recorder.start_recording()
        
        # Listen for ESC key to stop
        stop_event = threading.Event()
        
        def on_press(key):
            if key == keyboard.Key.esc:
                stop_event.set()
                return False  # Stop listener
        
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        
        # Wait for ESC
        stop_event.wait()
        
        # Stop recording
        filepath = recorder.stop_recording(name)
        self.is_recording = False
        
        self.log_system(f"✅ Recording saved: {name}")
        tts_speak(f"Recording saved as {name}", priority=True)
        self.set_status("🟢 Ready", "#666666")
        
        # Update button and refresh list
        self.q.put(('update_record_btn', '⏺ Record', '#ff4444'))
        self.q.put(('refresh_tasks',))
    
    def _play_selected_task(self, event=None):
        """Play the selected recording with countdown."""
        selection = self.tasks_listbox.curselection()
        if not selection:
            return
        
        item = self.tasks_listbox.get(selection[0])
        if item.startswith("("):  # Skip placeholder items
            return
        
        # Extract name (remove "▶ " prefix)
        name = item.replace("▶ ", "")
        
        # Start playback in separate thread
        threading.Thread(target=self._playback_countdown, args=(name,), daemon=True).start()
    
    def _playback_countdown(self, name):
        """Show countdown before playback starts."""
        from voice.tts import speak as tts_speak
        from recorder.action_player import get_player
        
        self.log_system(f"Preparing to play: {name}")
        tts_speak(f"Playing {name} in", priority=True)
        
        # 5 second countdown
        for i in range(5, 0, -1):
            self.log_system(f"Starting in {i}...")
            tts_speak(str(i), priority=True)
            time.sleep(1)
        
        self.log_system(f"▶ Playing: {name}")
        tts_speak("Starting playback", priority=True)
        self.set_status("▶ Playing...", "#00ffff")
        
        # Play recording
        player = get_player()
        success = player.play(name)
        
        if success:
            self.log_system(f"✅ Playback complete: {name}")
            tts_speak("Playback complete", priority=True)
        else:
            self.log_system(f"❌ Playback failed: {name}")
            tts_speak("Playback failed", priority=True)
        
        self.set_status("🟢 Ready", "#666666")

    # Dragging logic
    def start_move(self, event): 
        self.x = event.x
        self.y = event.y
    
    def stop_move(self, event): 
        self.x = None
        self.y = None
    
    def do_move(self, event):
        x = self.winfo_x() + (event.x - self.x)
        y = self.winfo_y() + (event.y - self.y)
        self.geometry(f"+{x}+{y}")