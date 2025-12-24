"""Quick test for browser-based email"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.communication import send_email_browser

result = send_email_browser(
    to="parth23100@gmail.com",
    subject="Test from SAGE",
    body="Hello, this is a test email from SAGE. The body should now appear automatically."
)
print(result)
