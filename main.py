"""
SAGE - Smart Agent for General Execution
Entry point for the application.
"""

import sys
import argparse
import threading
from ui import MainWindow
from core.task_executor import get_executor
from voice.assistant import get_assistant

def run_cli():
    """Run in Command Line Interface mode."""
    print("SAGE CLI Mode")
    print("Type 'exit' to quit.")
    
    executor = get_executor()
    
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() in ['exit', 'quit']:
                break
                
            result = executor.execute(user_input)
            
            if result.get('response'):
                print(f"SAGE: {result['response']}")
            elif result.get('message'):
                print(f"SAGE: {result['message']}")
            elif result.get('result'):
                print(f"Result: {result['result']}")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

def run_gui():
    """Run graphical interface."""
    app = MainWindow()
    app.start()

def main():
    parser = argparse.ArgumentParser(description="SAGE Desktop Assistant")
    parser.add_argument('--cli', action='store_true', help="Run in CLI mode")
    parser.add_argument('--voice', action='store_true', help="Start voice assistant immediately (CLI only)")
    
    args = parser.parse_args()
    
    if args.cli:
        if args.voice:
            # Start voice loop
            get_assistant().start()
        else:
            run_cli()
    else:
        run_gui()

if __name__ == "__main__":
    main()
