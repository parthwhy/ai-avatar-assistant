"""
Main Window Bridge
Redirects to ParticleWindow.
"""

from .particle_window import ParticleWindow

class MainWindow:
    """Wrapper to maintain interface compatibility with main.py"""
    def start(self):
        app = ParticleWindow()
        app.mainloop()
