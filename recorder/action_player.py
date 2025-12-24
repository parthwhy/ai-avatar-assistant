"""
Action Player
Replays recorded mouse and keyboard events.
"""

import time
import json
import threading
from pynput import mouse, keyboard
from config.settings import settings

class ActionPlayer:
    """Replays events captured by ActionRecorder."""
    
    def __init__(self):
        self.mouse_ctl = mouse.Controller()
        self.key_ctl = keyboard.Controller()
        self.playing = False
        
    def list_recordings(self) -> list:
        """Get list of available recordings."""
        files = []
        if settings.recordings_dir.exists():
            for f in settings.recordings_dir.glob("*.json"):
                files.append(f.stem)
        return files
        
    def play(self, recording_name: str) -> bool:
        """
        Replay a recording.
        
        Args:
            recording_name: Name of file (without .json)
            
        Returns:
            True if successful
        """
        filepath = settings.recordings_dir / f"{recording_name}.json"
        
        if not filepath.exists():
            print(f"Recording '{recording_name}' not found.")
            return False
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            events = data.get('events', [])
            if not events:
                print("Empty recording.")
                return False
                
            self.playing = True
            print(f"Playing '{recording_name}'...")
            
            # Replay events
            start_time = time.time()
            
            # Simple replay loop
            # Optimize: Use relative delays
            previous_event_time = 0
            
            for event in events:
                if not self.playing:
                    break
                    
                # Wait for target time
                event_time = event['time']
                delay = event_time - previous_event_time
                if delay > 0:
                    time.sleep(delay)
                    
                previous_event_time = event_time
                
                self._execute_event(event)
                
            print("Playback finished.")
            self.playing = False
            return True
            
        except Exception as e:
            print(f"Error during playback: {e}")
            self.playing = False
            return False
            
    def _execute_event(self, event):
        """Execute a single event."""
        etype = event['type']
        
        if etype == 'click':
            # Move mouse first
            self.mouse_ctl.position = (event['x'], event['y'])
            
            # Determine button
            btn = mouse.Button.left
            if 'right' in event['button']: btn = mouse.Button.right
            elif 'middle' in event['button']: btn = mouse.Button.middle
            
            if event['pressed']:
                self.mouse_ctl.press(btn)
            else:
                self.mouse_ctl.release(btn)
                
        elif etype == 'scroll':
            self.mouse_ctl.position = (event['x'], event['y'])
            self.mouse_ctl.scroll(event['dx'], event['dy'])
            
        elif etype == 'key_press' or etype == 'key_release':
            k = event['key']
            
            # Handle special keys string representation
            key_obj = k
            if len(k) > 1 and 'Key.' in k:
                # Convert string 'Key.enter' to keyboard.Key.enter
                attr = k.split('.')[1]
                if hasattr(keyboard.Key, attr):
                    key_obj = getattr(keyboard.Key, attr)
            
            if etype == 'key_press':
                self.key_ctl.press(key_obj)
            else:
                self.key_ctl.release(key_obj)

# Global instance
_player = None

def get_player():
    global _player
    if _player is None:
        _player = ActionPlayer()
    return _player
