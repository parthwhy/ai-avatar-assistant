"""
SAGE Dynamic Island UI
Modern, minimalist always-on-top widget inspired by Dynamic Island design.
"""

import sys
import os
import threading
import time
from PyQt6.QtCore import Qt, QPoint, QSize, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPainter, QPainterPath, QAction
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QLabel, QGraphicsDropShadowEffect, QFrame, QSizePolicy,
    QTextEdit, QListWidget
)

# Import SAGE components
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.task_executor import get_executor
from voice import listen
from voice.wake_word import get_detector
from voice.tts import speak as tts_speak

# --- Constants for Styling ---
DARK_BG = "#121212"      # Deep black background
CONTAINER_BG = "#1E1E1E" # SAGE dark theme
ACCENT_GREEN = "#39FF14" # Neon green accent
SAGE_BLUE = "#88ccff"    # SAGE blue accent
TEXT_WHITE = "#FFFFFF"
TEXT_GRAY = "#A0A0A0"
CORNER_RADIUS = "30px"   # Heavily rounded corners


class SAGEDynamicIsland(QMainWindow):
    """SAGE AI Assistant - Dynamic Island Style Interface"""
    
    def __init__(self):
        super().__init__()
        
        # Window setup for always on top and frameless
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |  # Remove OS title bar
            Qt.WindowType.WindowStaysOnTopHint | # Always on top
            Qt.WindowType.Tool                   # Hide from taskbar
        )
        
        # Make background transparent for rounded corners
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # State variables
        self.is_expanded = False
        self.is_listening = False
        self.is_processing = False
        self.drag_pos = QPoint()
        
        # SAGE components
        self.executor = get_executor()
        
        # Initialize UI
        self.init_ui()
        self.setup_styling()
        
        # Animation timers
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.animate_logo_pulse)
        self.pulse_phase = True
        
        # Start voice detection
        self.start_voice_loop()
    
    def init_ui(self):
        """Initialize the user interface elements."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # --- The Dynamic Island Pill (Collapsed View) ---
        self.pill_container = QFrame()
        self.pill_container.setObjectName("PillContainer")
        self.pill_container.setFixedHeight(60)
        
        pill_layout = QHBoxLayout(self.pill_container)
        pill_layout.setContentsMargins(15, 10, 15, 10)
        pill_layout.setSpacing(15)
        
        # 1. SAGE Logo (with pulsing animation)
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(40, 40)
        
        # Load logo.png or create placeholder
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(
                40, 40, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
        else:
            # Create SAGE placeholder logo
            pixmap = QPixmap(40, 40)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(QColor(SAGE_BLUE))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(0, 0, 40, 40)
            painter.setPen(QColor(TEXT_WHITE))
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "S")
            painter.end()
        
        self.logo_label.setPixmap(pixmap)
        
        # Create glow effect for listening state
        self.logo_shadow = QGraphicsDropShadowEffect()
        self.logo_shadow.setBlurRadius(0)
        self.logo_shadow.setColor(QColor(ACCENT_GREEN))
        self.logo_shadow.setOffset(0, 0)
        self.logo_label.setGraphicsEffect(self.logo_shadow)
        
        pill_layout.addWidget(self.logo_label)
        
        # Status indicator text
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("StatusLabel")
        pill_layout.addWidget(self.status_label)
        
        # Spacer to push buttons to the right
        pill_layout.addStretch()
        
        # 2. Stop Button (Stop speaking and return to sleep)
        self.stop_btn = QPushButton("⏹")
        self.stop_btn.setObjectName("IconButton")
        self.stop_btn.setToolTip("Stop Speaking & Sleep")
        self.stop_btn.clicked.connect(self.stop_and_sleep)
        pill_layout.addWidget(self.stop_btn)
        
        # 3. Expand/Minimize Button
        self.expand_btn = QPushButton("↕")
        self.expand_btn.setObjectName("IconButton")
        self.expand_btn.setToolTip("Expand/Collapse Interface")
        self.expand_btn.clicked.connect(self.toggle_expand)
        pill_layout.addWidget(self.expand_btn)
        
        # 4. Close Button
        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("CloseButton")
        self.close_btn.setToolTip("Close SAGE")
        self.close_btn.clicked.connect(self.close_application)
        pill_layout.addWidget(self.close_btn)
        
        self.main_layout.addWidget(self.pill_container)
        
        # --- Expanded Interface (Hidden by default) ---
        self.expanded_view = QFrame()
        self.expanded_view.setObjectName("ExpandedView")
        self.expanded_view.hide()
        
        expanded_layout = QVBoxLayout(self.expanded_view)
        expanded_layout.setContentsMargins(20, 20, 20, 20)
        
        # Chat area
        self.chat_area = QTextEdit()
        self.chat_area.setObjectName("ChatArea")
        self.chat_area.setMaximumHeight(200)
        self.chat_area.setReadOnly(True)
        expanded_layout.addWidget(QLabel("💬 Chat History"))
        expanded_layout.addWidget(self.chat_area)
        
        # Tasks area
        self.tasks_list = QListWidget()
        self.tasks_list.setObjectName("TasksList")
        self.tasks_list.setMaximumHeight(150)
        expanded_layout.addWidget(QLabel("📋 Recent Tasks"))
        expanded_layout.addWidget(self.tasks_list)
        
        self.main_layout.addWidget(self.expanded_view)
    
    def setup_styling(self):
        """Apply modern styling to the interface."""
        qss = f"""
        QWidget {{
            font-family: 'Segoe UI', 'Roboto', sans-serif;
        }}
        
        #PillContainer {{
            background-color: {CONTAINER_BG};
            border-radius: 30px;
            border: 1px solid #333333;
        }}
        
        #StatusLabel {{
            color: {TEXT_WHITE};
            font-size: 12px;
            font-weight: 500;
        }}
        
        #ExpandedView {{
            background-color: {CONTAINER_BG};
            border-radius: 20px;
            margin-top: 10px;
            border: 1px solid #333333;
        }}
        
        #IconButton {{
            background-color: transparent;
            color: {TEXT_WHITE};
            border: none;
            font-size: 16px;
            padding: 8px;
            border-radius: 15px;
            min-width: 30px;
            min-height: 30px;
        }}
        
        #IconButton:hover {{
            background-color: #404040;
        }}
        
        #CloseButton {{
            background-color: transparent;
            color: {TEXT_GRAY};
            border: none;
            font-size: 14px;
            font-weight: bold;
            padding: 8px;
            border-radius: 15px;
            min-width: 30px;
            min-height: 30px;
        }}
        
        #CloseButton:hover {{
            color: #FF5555;
            background-color: #404040;
        }}
        
        #ChatArea {{
            background-color: {DARK_BG};
            color: {TEXT_WHITE};
            border: 1px solid #333333;
            border-radius: 10px;
            padding: 10px;
            font-size: 11px;
        }}
        
        #TasksList {{
            background-color: {DARK_BG};
            color: {TEXT_WHITE};
            border: 1px solid #333333;
            border-radius: 10px;
            font-size: 11px;
        }}
        
        QLabel {{
            color: {TEXT_WHITE};
            font-size: 12px;
            font-weight: 500;
        }}
        """
        
        self.setStyleSheet(qss)
        
        # Set initial size
        self.resize(320, 60)
    
    def start_voice_loop(self):
        """Start the voice detection loop in background."""
        def voice_thread():
            try:
                detector = get_detector()
                detector.start_listening(callback=self.on_wake_word)
            except Exception as e:
                print(f"Voice detection error: {e}")
        
        threading.Thread(target=voice_thread, daemon=True).start()
    
    def on_wake_word(self):
        """Called when wake word is detected."""
        if self.is_processing:
            return
        
        self.set_listening_state(True)
        self.update_status("Listening...")
        
        # Respond with "Yes, I'm listening"
        tts_speak("Yes, I'm listening", priority=True)
        time.sleep(0.5)
        
        # Listen for command
        cmd = listen(timeout=3, phrase_time_limit=8)
        
        if cmd and not self.is_processing:
            self.set_processing_state(True)
            self.update_status("Processing...")
            self.add_to_chat(f"USER: {cmd}")
            
            # Execute command
            result = self.executor.execute(cmd)
            
            # Extract response
            response = self.extract_response(result)
            self.add_to_chat(f"SAGE: {response}")
            
            # Speak response
            if response:
                tts_speak(response, priority=True)
                time.sleep(1)
                tts_speak("Listening for your next command", priority=False)
            
            self.set_processing_state(False)
        else:
            self.add_to_chat("No command detected")
            tts_speak("I didn't catch that. Say the wake word to try again.", priority=True)
        
        self.set_listening_state(False)
        self.update_status("Ready")
    
    def set_listening_state(self, listening):
        """Set the listening state and start/stop animations."""
        self.is_listening = listening
        
        if listening:
            self.pulse_timer.start(800)
            self.update_status("🎤 Listening...")
        else:
            self.pulse_timer.stop()
            self.logo_shadow.setBlurRadius(0)
    
    def set_processing_state(self, processing):
        """Set the processing state."""
        self.is_processing = processing
        
        if processing:
            self.update_status("🧠 Processing...")
        else:
            self.update_status("Ready")
    
    def animate_logo_pulse(self):
        """Animate the logo with pulsing glow effect."""
        if self.pulse_phase:
            radius = 20
            opacity = 180
        else:
            radius = 5
            opacity = 80
        
        color = QColor(ACCENT_GREEN)
        color.setAlpha(opacity)
        self.logo_shadow.setColor(color)
        
        # Animate blur radius
        self.animation = QPropertyAnimation(self.logo_shadow, b"blurRadius")
        self.animation.setDuration(600)
        self.animation.setStartValue(self.logo_shadow.blurRadius())
        self.animation.setEndValue(radius)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.start()
        
        self.pulse_phase = not self.pulse_phase
    
    def stop_and_sleep(self):
        """Stop current TTS and return to sleep state."""
        try:
            from voice.tts import stop_speech
            stop_speech()
            
            self.set_listening_state(False)
            self.set_processing_state(False)
            self.update_status("Stopped")
            
            # Brief feedback
            threading.Timer(1.0, lambda: self.update_status("Ready")).start()
            
        except Exception as e:
            print(f"Stop error: {e}")
    
    def toggle_expand(self):
        """Toggle between pill and expanded view."""
        self.is_expanded = not self.is_expanded
        
        if self.is_expanded:
            self.expanded_view.show()
            self.resize(400, self.sizeHint().height() + 250)
            self.expand_btn.setText("↑")
        else:
            self.expanded_view.hide()
            self.resize(320, 60)
            self.expand_btn.setText("↕")
    
    def update_status(self, status):
        """Update the status label."""
        self.status_label.setText(status)
    
    def add_to_chat(self, message):
        """Add message to chat area."""
        if hasattr(self, 'chat_area'):
            self.chat_area.append(message)
            # Keep only last 10 messages
            text = self.chat_area.toPlainText()
            lines = text.split('\n')
            if len(lines) > 20:
                self.chat_area.setPlainText('\n'.join(lines[-20:]))
    
    def extract_response(self, result):
        """Extract response from execution result."""
        if isinstance(result, dict):
            if result.get('response'):
                return result['response']
            elif result.get('message'):
                return result['message']
            elif result.get('success'):
                return "Task completed successfully"
        return "Command executed"
    
    def close_application(self):
        """Close the application."""
        QApplication.instance().quit()
    
    # --- Window dragging functionality ---
    def mousePressEvent(self, event):
        """Handle mouse press for dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging."""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()


def main():
    """Main function to run the SAGE Dynamic Island."""
    app = QApplication(sys.argv)
    
    # Create the dynamic island
    island = SAGEDynamicIsland()
    
    # Position at top center of screen
    screen = app.primaryScreen().availableGeometry()
    x = (screen.width() - island.width()) // 2
    island.move(x, 50)
    
    island.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()