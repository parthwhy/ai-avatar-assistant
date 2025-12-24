"""
Tool Generator
Allows SAGE to create new Python tools dynamically using AI.
"""

from typing import Dict, Optional
import os
import re
from core.brain import get_brain
from pathlib import Path

# Path to save generated tools
GENERATED_TOOLS_DIR = Path(__file__).parent.parent.parent / 'data' / 'generated_tools'
GENERATED_TOOLS_DIR.mkdir(parents=True, exist_ok=True)

# Add to path so they can be imported
import sys
if str(GENERATED_TOOLS_DIR) not in sys.path:
    sys.path.append(str(GENERATED_TOOLS_DIR))

def generate_tool(name: str, description: str, usage_example: str) -> Dict[str, any]:
    """
    Generate a new Python tool using AI.
    
    Args:
        name: Name of the tool (e.g., 'currency_converter')
        description: What the tool should do
        usage_example: How to use it
    
    Returns:
        Result dictionary with path to new file
    """
    brain = get_brain()
    
    prompt = f"""Write a Python function for a tool called '{name}'.
    
Description: {description}

Requirements:
- Function should be named '{name}'
- Type hints for all arguments and return values
- Docstring explaining usage
- Handle errors gracefully
- Return a dictionary with {{'success': True/False, 'result': ..., 'message': ...}}
- Use only standard library or common packages (requests, beautifulsoup4, etc.)
- If using external packages, try to import them inside the function so it doesn't break if missing

Example usage: {usage_example}

Respond with ONLY the Python code:"""

    result = brain.ask(prompt)
    
    if not result['success']:
        return result
        
    code = result['response']
    
    # Extract code from markdown
    if '```python' in code:
        code = code.split('```python')[1].split('```')[0].strip()
    elif '```' in code:
        code = code.split('```')[1].split('```')[0].strip()
        
    # Save to file
    filename = f"{name}.py"
    filepath = GENERATED_TOOLS_DIR / filename
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
            
        return {
            'success': True,
            'message': f"Tool '{name}' created successfully.",
            'path': str(filepath),
            'code_preview': code[:100] + "..."
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f"Failed to save tool: {str(e)}"
        }

def list_generated_tools() -> Dict[str, any]:
    """List all tools created by AI."""
    try:
        tools = []
        for f in GENERATED_TOOLS_DIR.glob('*.py'):
            if f.name != '__init__.py':
                tools.append(f.name)
        return {
            'success': True,
            'tools': tools,
            'count': len(tools)
        }
    except Exception as e:
        return {
            'success': False,
            'message': f"Error listing tools: {e}"
        }
