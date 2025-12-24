"""
Action Recorder
Records mouse clicks and keyboard events for playback.
Uses pynput for robust hook-based recording.
"""

import time
import json
import threading
from typing import List, Dict, Any
from pynput import mouse, keyboard
from pathlib import Path
from config.settings import settings

class ActionRecorder:
    """Record and save user input macros."""
    
    def __init__(self):
        self.recording = False
        self.events: List[Dict[str, Any]] = []
        self.start_time = 0
        self.mouse_listener = None
        self.key_listener = None
        
        # Ensure directory exists
        path = settings.recordings_dir
        path.mkdir(parents=True, exist_ok=True)
        
    def start_recording(self):
        """Start capturing events."""
        if self.recording:
            return
            
        self.events = []
        self.recording = True
        self.start_time = time.time()
        
        # Start listeners non-blocking
        self.mouse_listener = mouse.Listener(
            on_click=self._on_click,
            on_scroll=self._on_scroll
        )
        self.key_listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        
        self.mouse_listener.start()
        self.key_listener.start()
        
        print("Recording started... (Press ESC to stop in CLI mode)")

    def stop_recording(self, filename: str) -> str:
        """
        Stop recording and save to file.
        
        Args:
            filename: Name of the recording (without extension)
            
        Returns:
            Path to saved file
        """
        if not self.recording:
            return ""
            
        self.recording = False
        
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.key_listener:
            self.key_listener.stop()
            
        # Optimize: Remove consecutive duplicate moves (if we were tracking moves)
        # But we only track clicks/scroll/keys for now to keep size down
        
        filepath = settings.recordings_dir / f"{filename}.json"
        
        data = {
            "name": filename,
            "duration": time.time() - self.start_time,
            "events": self.events
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        return str(filepath)

    def _on_click(self, x, y, button, pressed):
        if not self.recording: return
        self.events.append({
            "type": "click",
            "time": time.time() - self.start_time,
            "x": x,
            "y": y,
            "button": str(button),
            "pressed": pressed
        })

    def _on_scroll(self, x, y, dx, dy):
        if not self.recording: return
        self.events.append({
            "type": "scroll",
            "time": time.time() - self.start_time,
            "x": x,
            "y": y,
            "dx": dx,
            "dy": dy
        })

    def _on_press(self, key):
        if not self.recording: return
        try:
            k = key.char
        except AttributeError:
            k = str(key)
            
        self.events.append({
            "type": "key_press",
            "time": time.time() - self.start_time,
            "key": k
        })

    def _on_release(self, key):
        if not self.recording: return
        # Stop recording on ESC
        if key == keyboard.Key.esc:
            # We don't stop here automatically, main loop handles it
            pass
            
        try:
            k = key.char
        except AttributeError:
            k = str(key)
            
        self.events.append({
            "type": "key_release",
            "time": time.time() - self.start_time,
            "key": k
        })

# Global instance
_recorder = None

def get_recorder():
    global _recorder
    if _recorder is None:
        _recorder = ActionRecorder()
    return _recorder
