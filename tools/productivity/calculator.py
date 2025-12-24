"""
Calculator Tool
Safe math expression evaluation.
"""

import math
import re
from typing import Dict, Union


# Safe math functions and constants
SAFE_FUNCTIONS = {
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
    'sum': sum,
    'pow': pow,
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,
    'log10': math.log10,
    'log2': math.log2,
    'exp': math.exp,
    'floor': math.floor,
    'ceil': math.ceil,
    'factorial': math.factorial,
    'gcd': math.gcd,
    'pi': math.pi,
    'e': math.e,
}


def calculate(expression: str) -> Dict[str, any]:
    """
    Evaluate a mathematical expression safely.
    
    Args:
        expression: Math expression like "15% of 2400" or "sqrt(16) + 5"
    
    Returns:
        Dictionary with result or error.
    """
    try:
        # Convert natural language patterns
        expr = _normalize_expression(expression)
        
        # Evaluate safely
        result = evaluate_expression(expr)
        
        return {
            'success': True,
            'result': result,
            'expression': expression,
            'normalized': expr,
            'message': f'{expression} = {result}'
        }
    except ZeroDivisionError:
        return {
            'success': False,
            'message': 'Division by zero',
            'error': 'Division by zero'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Could not calculate: {str(e)}',
            'error': str(e)
        }


def _normalize_expression(expr: str) -> str:
    """
    Convert natural language math to Python expression.
    
    Examples:
        "15% of 2400" -> "(15/100)*2400"
        "2 squared" -> "2**2"
        "square root of 16" -> "sqrt(16)"
    """
    expr = expr.lower().strip()
    
    # Percentage patterns
    # "15% of 2400" -> "(15/100)*2400"
    percent_of = re.search(r'(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)', expr)
    if percent_of:
        pct = percent_of.group(1)
        num = percent_of.group(2)
        return f'({pct}/100)*{num}'
    
    # "what is 15% of 2400" variation
    percent_of2 = re.search(r'what\s+is\s+(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)', expr)
    if percent_of2:
        pct = percent_of2.group(1)
        num = percent_of2.group(2)
        return f'({pct}/100)*{num}'
    
    # Simple percentage "15%" -> "15/100"
    expr = re.sub(r'(\d+(?:\.\d+)?)\s*%', r'(\1/100)', expr)
    
    # "squared" -> "**2"
    expr = re.sub(r'(\d+(?:\.\d+)?)\s*squared', r'\1**2', expr)
    
    # "cubed" -> "**3"
    expr = re.sub(r'(\d+(?:\.\d+)?)\s*cubed', r'\1**3', expr)
    
    # "to the power of X" -> "**X"
    expr = re.sub(r'to\s+the\s+power\s+of\s+(\d+)', r'**\1', expr)
    
    # "square root of X" -> "sqrt(X)"
    expr = re.sub(r'square\s*root\s*of\s*(\d+(?:\.\d+)?)', r'sqrt(\1)', expr)
    
    # "X times Y" -> "X*Y"
    expr = re.sub(r'(\d+(?:\.\d+)?)\s*times\s*(\d+(?:\.\d+)?)', r'\1*\2', expr)
    
    # "X plus Y" -> "X+Y"
    expr = re.sub(r'(\d+(?:\.\d+)?)\s*plus\s*(\d+(?:\.\d+)?)', r'\1+\2', expr)
    
    # "X minus Y" -> "X-Y"
    expr = re.sub(r'(\d+(?:\.\d+)?)\s*minus\s*(\d+(?:\.\d+)?)', r'\1-\2', expr)
    
    # "X divided by Y" -> "X/Y"
    expr = re.sub(r'(\d+(?:\.\d+)?)\s*divided\s*by\s*(\d+(?:\.\d+)?)', r'\1/\2', expr)
    
    # Remove "what is", "calculate", etc.
    expr = re.sub(r'^(what\s+is|calculate|compute|evaluate)\s*', '', expr)
    
    # Replace x with * for multiplication
    expr = re.sub(r'(\d)\s*x\s*(\d)', r'\1*\2', expr)
    
    return expr.strip()


def evaluate_expression(expr: str) -> Union[int, float]:
    """
    Safely evaluate a mathematical expression.
    Only allows numbers, operators, and safe math functions.
    
    Args:
        expr: Python-style math expression
    
    Returns:
        Numeric result
    
    Raises:
        ValueError: If expression contains unsafe elements
    """
    # Validate expression - only allow safe characters
    allowed_chars = set('0123456789+-*/.()[], ')
    allowed_chars.update(set('abcdefghijklmnopqrstuvwxyz_'))
    
    if not all(c in allowed_chars for c in expr.lower()):
        raise ValueError(f"Expression contains invalid characters")
    
    # Check for potentially dangerous patterns
    dangerous_patterns = [
        '__', 'import', 'exec', 'eval', 'open', 'file',
        'input', 'raw_input', 'compile', 'globals', 'locals',
        'getattr', 'setattr', 'delattr', 'dir', 'vars'
    ]
    
    expr_lower = expr.lower()
    for pattern in dangerous_patterns:
        if pattern in expr_lower:
            raise ValueError(f"Expression contains forbidden pattern: {pattern}")
    
    # Evaluate with only safe functions available
    try:
        result = eval(expr, {"__builtins__": {}}, SAFE_FUNCTIONS)
        
        # Round floating point errors
        if isinstance(result, float):
            # If very close to an integer, return integer
            if abs(result - round(result)) < 1e-10:
                return int(round(result))
            # Otherwise round to reasonable precision
            return round(result, 10)
        
        return result
    except NameError as e:
        raise ValueError(f"Unknown function or variable: {e}")
