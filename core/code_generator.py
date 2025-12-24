"""
Code Generator Agent
Creates PyAutoGUI automation code when no existing tool can handle a task.
Uses OpenRouter with Qwen3 Coder for expert code generation.
Saves generated tools for future reuse.
"""

import os
import re
import json
import time
import requests
from pathlib import Path
from typing import Dict, Any, List
from config.settings import settings


class CodeGeneratorAgent:
    """
    Generates PyAutoGUI automation code for tasks that don't have existing tools.
    Uses OpenRouter API with Qwen3 Coder 480B for expert code generation.
    """
    
    def __init__(self):
        # Use OpenRouter API for Qwen3 Coder
        self.openrouter_api_key = getattr(settings, 'openrouter_api_key', None) or os.getenv('OPENROUTER_API_KEY')
        self.model = "qwen/qwen-2.5-coder-32b-instruct"  # Qwen 2.5 Coder 32B (working model)
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.generated_tools_dir = settings.generated_tools_dir
        self.dangerous_operations = [
            'shutdown', 'restart', 'delete', 'remove', 'rmdir', 'rm ', 'del ',
            'format', 'fdisk', 'diskpart', 'registry', 'regedit', 'taskkill',
            'net user', 'net localgroup', 'chmod 777', 'sudo rm', 'dd if=',
            'mkfs', 'fsck', 'mount', 'umount', 'kill -9', 'killall'
        ]
        
        # Ensure generated tools directory exists
        self.generated_tools_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing generated tools
        self.load_generated_tools()
    
    def load_generated_tools(self):
        """Load previously generated tools from disk."""
        self.generated_tools = {}
        
        if not self.generated_tools_dir.exists():
            return
        
        for tool_file in self.generated_tools_dir.glob("*.py"):
            try:
                # Read the tool metadata from comments
                with open(tool_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract metadata from comments
                if '# TOOL_NAME:' in content:
                    tool_name = content.split('# TOOL_NAME:')[1].split('\n')[0].strip()
                    description = ''
                    if '# DESCRIPTION:' in content:
                        description = content.split('# DESCRIPTION:')[1].split('\n')[0].strip()
                    
                    self.generated_tools[tool_name] = {
                        'file': tool_file,
                        'description': description,
                        'content': content
                    }
            except Exception as e:
                print(f"Warning: Could not load generated tool {tool_file}: {e}")
    
    def can_generate_tool(self, task_description: str) -> bool:
        """
        Check if we can generate a tool for this task.
        
        Args:
            task_description: Description of what the user wants to do
            
        Returns:
            True if we can generate a tool, False otherwise
        """
        if not self.openrouter_api_key:
            return False
        
        # Check if it's something that can be automated with PyAutoGUI
        automation_keywords = [
            'click', 'type', 'press', 'key', 'mouse', 'screen', 'window',
            'button', 'menu', 'dialog', 'form', 'input', 'select', 'drag',
            'scroll', 'screenshot', 'find', 'locate', 'image', 'text',
            'open', 'close', 'minimize', 'maximize', 'move', 'resize'
        ]
        
        task_lower = task_description.lower()
        return any(keyword in task_lower for keyword in automation_keywords)
    
    def generate_tool(self, task_description: str, function_name: str = None) -> Dict[str, Any]:
        """
        Generate a PyAutoGUI tool for the given task using Qwen3 Coder.
        
        Args:
            task_description: What the user wants to automate
            function_name: Optional name for the function (auto-generated if None)
            
        Returns:
            Dictionary with generation result
        """
        if not self.openrouter_api_key:
            return {
                'success': False,
                'message': 'Code generator offline (no OpenRouter API key). Set OPENROUTER_API_KEY in .env'
            }
        
        # Generate function name if not provided
        if not function_name:
            function_name = self._generate_function_name(task_description)
        
        # Check if we already have this tool
        if function_name in self.generated_tools:
            return {
                'success': True,
                'message': f'Tool {function_name} already exists',
                'function_name': function_name,
                'file_path': str(self.generated_tools[function_name]['file']),
                'reused': True
            }
        
        # Detailed expert prompt for Qwen Coder
        system_prompt = """You are an EXPERT Python automation engineer. Generate ONLY Python code, NO explanations, NO thinking, NO markdown.

CRITICAL RULES:
1. Output ONLY Python code - no text before or after
2. NO <think> tags or reasoning - just code
3. Use PyAutoGUI for automation
4. Include proper error handling
5. Return dict with 'success' and 'message' keys

PYAUTOGUI REFERENCE:
- pyautogui.click(x, y) - Click at position
- pyautogui.press('key') - Press key
- pyautogui.hotkey('ctrl', 'c') - Key combination
- pyautogui.size() - Get screen size
- pyautogui.scroll(clicks) - Scroll

OUTPUT ONLY CODE - NO EXPLANATIONS"""

        user_prompt = f"""Task: {task_description}
Function name: {function_name}

Generate Python code using this exact template:

import pyautogui
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

def {function_name}(**kwargs):
    \"\"\"
    {task_description}
    \"\"\"
    try:
        # Your automation code here
        
        return {{
            'success': True,
            'message': 'Task completed successfully'
        }}
    except pyautogui.FailSafeException:
        return {{
            'success': False,
            'message': 'Automation aborted (mouse moved to corner)'
        }}
    except Exception as e:
        return {{
            'success': False,
            'message': f'Error: {{str(e)}}'
        }}

OUTPUT ONLY CODE - NO EXPLANATIONS"""

        try:
            # Call OpenRouter API
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://sage-assistant.local",
                "X-Title": "SAGE AI Assistant"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.2,
                "max_tokens": 2000
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            generated_code = result['choices'][0]['message']['content']
            
            # Clean up the code (remove markdown if present)
            if '```python' in generated_code:
                generated_code = generated_code.split('```python')[1].split('```')[0].strip()
            elif '```' in generated_code:
                generated_code = generated_code.split('```')[1].split('```')[0].strip()
            
            # Safety check
            safety_result = self._check_code_safety(generated_code)
            if not safety_result['safe']:
                return {
                    'success': False,
                    'message': f'Generated code contains dangerous operations: {safety_result["issues"]}',
                    'code': generated_code,
                    'requires_approval': True
                }
            
            # Save the generated tool
            save_result = self._save_generated_tool(function_name, task_description, generated_code)
            
            if save_result['success']:
                return {
                    'success': True,
                    'message': f'Generated tool: {function_name}',
                    'function_name': function_name,
                    'file_path': save_result['file_path'],
                    'code': generated_code,
                    'reused': False
                }
            else:
                return save_result
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Code generation failed: {str(e)}'
            }
    
    def _generate_function_name(self, task_description: str) -> str:
        """Generate a valid Python function name from task description."""
        # Remove special characters and convert to snake_case
        name = re.sub(r'[^a-zA-Z0-9\s]', '', task_description.lower())
        name = re.sub(r'\s+', '_', name.strip())
        
        # Ensure it starts with a letter
        if name and name[0].isdigit():
            name = 'auto_' + name
        
        # Limit length
        if len(name) > 30:
            name = name[:30]
        
        # Fallback
        if not name:
            name = f'generated_tool_{int(time.time())}'
        
        return name
    
    def _check_code_safety(self, code: str) -> Dict[str, Any]:
        """
        Check if generated code contains dangerous operations.
        
        Args:
            code: Generated Python code
            
        Returns:
            Dictionary with safety assessment
        """
        code_lower = code.lower()
        found_issues = []
        
        for dangerous_op in self.dangerous_operations:
            if dangerous_op in code_lower:
                found_issues.append(dangerous_op)
        
        return {
            'safe': len(found_issues) == 0,
            'issues': found_issues
        }
    
    def _save_generated_tool(self, function_name: str, description: str, code: str) -> Dict[str, Any]:
        """
        Save generated tool to disk.
        
        Args:
            function_name: Name of the function
            description: Description of what it does
            code: Generated Python code
            
        Returns:
            Save result
        """
        try:
            # Create file with metadata
            file_content = f'''"""
Generated Tool: {function_name}
Auto-generated by SAGE Code Generator
"""

# TOOL_NAME: {function_name}
# DESCRIPTION: {description}
# GENERATED: {time.strftime("%Y-%m-%d %H:%M:%S")}

{code}
'''
            
            file_path = self.generated_tools_dir / f"{function_name}.py"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            # Add to our registry
            self.generated_tools[function_name] = {
                'file': file_path,
                'description': description,
                'content': file_content
            }
            
            return {
                'success': True,
                'message': f'Tool saved to {file_path}',
                'file_path': str(file_path)
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to save tool: {str(e)}'
            }
    
    def execute_generated_tool(self, function_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a previously generated tool.
        
        Args:
            function_name: Name of the tool to execute
            **kwargs: Parameters to pass to the tool
            
        Returns:
            Execution result
        """
        if function_name not in self.generated_tools:
            return {
                'success': False,
                'message': f'Generated tool {function_name} not found'
            }
        
        try:
            # Load and execute the tool
            tool_info = self.generated_tools[function_name]
            
            # Create a namespace and execute the code
            namespace = {}
            exec(tool_info['content'], namespace)
            
            # Get the function and call it
            if function_name in namespace:
                func = namespace[function_name]
                return func(**kwargs)
            else:
                return {
                    'success': False,
                    'message': f'Function {function_name} not found in generated code'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error executing generated tool: {str(e)}'
            }
    
    def list_generated_tools(self) -> List[Dict[str, Any]]:
        """List all generated tools."""
        return [
            {
                'name': name,
                'description': info['description'],
                'file': str(info['file'])
            }
            for name, info in self.generated_tools.items()
        ]


# Global instance
_code_generator = None

def get_code_generator() -> CodeGeneratorAgent:
    """Get or create the global code generator instance."""
    global _code_generator
    if _code_generator is None:
        _code_generator = CodeGeneratorAgent()
    return _code_generator