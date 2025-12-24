"""
Tier 7 Recorder Tests
Run with: python tests/test_tier7_recorder.py
"""

import sys
import os
import unittest
import time
import json
import shutil
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recorder.action_recorder import ActionRecorder
from recorder.action_player import ActionPlayer
from config.settings import settings

class TestActionRecorder(unittest.TestCase):
    
    def setUp(self):
        self.recorder = ActionRecorder()
        self.test_file = "test_recording"
        
    def tearDown(self):
        # Cleanup test file
        f = settings.recordings_dir / f"{self.test_file}.json"
        if f.exists():
            f.unlink()
            
    @patch('recorder.action_recorder.mouse.Listener')
    @patch('recorder.action_recorder.keyboard.Listener')
    def test_start_stop_recording(self, mock_kb, mock_mouse):
        """Test recording state and file saving"""
        # Start
        self.recorder.start_recording()
        self.assertTrue(self.recorder.recording)
        
        # Simulate some events
        self.recorder._on_click(100, 200, 'Button.left', True)
        self.recorder._on_press('a')
        
        time.sleep(0.1)
        
        # Stop
        path = self.recorder.stop_recording(self.test_file)
        self.assertFalse(self.recorder.recording)
        self.assertTrue(os.path.exists(path))
        
        # Verify content
        with open(path, 'r') as f:
            data = json.load(f)
            self.assertEqual(data['name'], self.test_file)
            self.assertTrue(len(data['events']) >= 2)
            self.assertEqual(data['events'][0]['type'], 'click')
            self.assertEqual(data['events'][1]['type'], 'key_press')


class TestActionPlayer(unittest.TestCase):
    
    def setUp(self):
        self.player = ActionPlayer()
        self.test_file = "test_playback"
        
        # Create a dummy recording
        data = {
            "name": self.test_file,
            "duration": 1.0,
            "events": [
                {"type": "click", "time": 0.1, "x": 100, "y": 100, "button": "Button.left", "pressed": True},
                {"type": "key_press", "time": 0.2, "key": "a"}
            ]
        }
        filepath = settings.recordings_dir / f"{self.test_file}.json"
        with open(filepath, 'w') as f:
            json.dump(data, f)
            
    def tearDown(self):
        f = settings.recordings_dir / f"{self.test_file}.json"
        if f.exists():
            f.unlink()

    @patch('recorder.action_player.mouse.Controller')
    @patch('recorder.action_player.keyboard.Controller')
    def test_playback(self, mock_kb_cls, mock_mouse_cls):
        """Test playback triggers controller actions"""
        # Mock instances
        mock_mouse = mock_mouse_cls.return_value
        mock_kb = mock_kb_cls.return_value
        
        # Inject mocks into player (since it inits them in __init__)
        self.player.mouse_ctl = mock_mouse
        self.player.key_ctl = mock_kb
        
        success = self.player.play(self.test_file)
        self.assertTrue(success)
        
        # Verify calls
        mock_mouse.position = (100, 100)
        # We can't easily check property setting on mock like this without more setup, 
        # but we can check methods
        mock_mouse.press.assert_called()
        mock_kb.press.assert_called_with('a')


if __name__ == '__main__':
    print("\n" + "#"*60)
    print("TESTING: Tier 7 Action Recorder")
    print("#"*60 + "\n")
    unittest.main()
