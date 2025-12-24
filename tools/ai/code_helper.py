"""
Code Helper Tool
Explains, generates, and fixes code using AI.
"""

from typing import Dict, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def explain_code(code: str, language: Optional[str] = None) -> Dict[str, any]:
    """
    Explain what a piece of code does.
    
    Args:
        code: Code to explain
        language: Programming language (auto-detected if not provided)
    
    Returns:
        Dictionary with explanation.
    """
    from core.brain import get_brain
    
    brain = get_brain()
    
    lang_hint = f" (Language: {language})" if language else ""
    
    prompt = f"""Explain what this code does in simple terms{lang_hint}:

```
{code}
```

Provide:
1. A brief summary (1-2 sentences)
2. Step-by-step explanation
3. Any potential issues or improvements"""
    
    result = brain.ask(prompt)
    
    if result['success']:
        return {
            'success': True,
            'explanation': result['response'],
            'code_length': len(code),
            'message': 'Code explained'
        }
    
    return result


def generate_code(description: str, language: str = "python") -> Dict[str, any]:
    """
    Generate code from a description.
    
    Args:
        description: What the code should do
        language: Programming language to use
    
    Returns:
        Dictionary with generated code.
    """
    from core.brain import get_brain
    
    brain = get_brain()
    
    prompt = f"""Generate {language} code for the following:

{description}

Requirements:
- Write clean, well-commented code
- Include error handling where appropriate
- Make it production-ready

Respond with ONLY the code, wrapped in appropriate markdown code blocks."""
    
    result = brain.ask(prompt)
    
    if result['success']:
        # Extract code from markdown if present
        code = result['response']
        if '```' in code:
            # Find code between backticks
            import re
            code_match = re.search(r'```(?:\w+)?\n(.*?)```', code, re.DOTALL)
            if code_match:
                code = code_match.group(1)
        
        return {
            'success': True,
            'code': code.strip(),
            'language': language,
            'full_response': result['response'],
            'message': f'{language} code generated'
        }
    
    return result


def fix_code(code: str, error: Optional[str] = None, language: Optional[str] = None) -> Dict[str, any]:
    """
    Fix or improve code.
    
    Args:
        code: Code to fix
        error: Error message if any
        language: Programming language
    
    Returns:
        Dictionary with fixed code.
    """
    from core.brain import get_brain
    
    brain = get_brain()
    
    error_context = f"\n\nError message:\n{error}" if error else ""
    lang_hint = f" ({language})" if language else ""
    
    prompt = f"""Fix this code{lang_hint}:{error_context}

```
{code}
```

Provide:
1. The fixed code
2. Explanation of what was wrong
3. Any additional improvements made"""
    
    result = brain.ask(prompt)
    
    if result['success']:
        # Extract code from markdown if present
        response = result['response']
        fixed_code = response
        
        if '```' in response:
            import re
            code_match = re.search(r'```(?:\w+)?\n(.*?)```', response, re.DOTALL)
            if code_match:
                fixed_code = code_match.group(1).strip()
        
        return {
            'success': True,
            'fixed_code': fixed_code,
            'explanation': response,
            'message': 'Code fixed'
        }
    
    return result


def review_code(code: str, language: Optional[str] = None) -> Dict[str, any]:
    """
    Review code for issues and improvements.
    
    Args:
        code: Code to review
        language: Programming language
    
    Returns:
        Dictionary with review feedback.
    """
    from core.brain import get_brain
    
    brain = get_brain()
    
    lang_hint = f" ({language})" if language else ""
    
    prompt = f"""Review this code{lang_hint} and provide feedback:

```
{code}
```

Analyze for:
1. **Bugs**: Any potential bugs or errors
2. **Security**: Security vulnerabilities
3. **Performance**: Performance issues
4. **Style**: Code style and best practices
5. **Suggestions**: Specific improvements

Be constructive and specific."""
    
    result = brain.ask(prompt)
    
    if result['success']:
        return {
            'success': True,
            'review': result['response'],
            'message': 'Code reviewed'
        }
    
    return result
