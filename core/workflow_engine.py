"""
Workflow Engine
Executes sequences of steps, passing data between them.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re

@dataclass
class WorkflowStep:
    tool: str
    params: Dict[str, Any]
    store_result: Optional[str] = None
    use_result_from: Optional[str] = None

class WorkflowEngine:
    """
    Executes a list of steps.
    Handles variable substitution (e.g. using output of step 1 in step 2).
    """
    
    def __init__(self):
        self.memory = {}
        
    def run(self, steps: List[WorkflowStep]) -> Dict[str, Any]:
        """
        Run a sequence of steps.
        
        Args:
            steps: List of WorkflowStep objects
            
        Returns:
            Result of the final step
        """
        self.memory = {} # Clear memory for new run
        final_result = None
        
        # Dynamic import of tools
        # (Ideally passed in or registered, but doing inline for simplicity per Phase 6 plan)
        from tools import system, productivity, communication, ai
        
        # Registry of available tools for workflows
        # This duplicates TaskExecutor map slightly, but keeps engine independent
        tool_registry = {
            'search_web': productivity.web_search.search_web,
            'summarize': ai.summarizer.summarize,
            'send_email_browser': communication.email_sender.send_email_browser,
            'open_app': system.app_launcher.open_app,
            'calculate': productivity.calculator.calculate,
            'weather': productivity.weather.get_weather,
            # Add others as needed
        }
        
        execution_log = []
        
        for i, step in enumerate(steps):
            try:
                # 1. Resolve parameters (substitute variables)
                resolved_params = self._resolve_params(step.params)
                
                # 2. Get tool
                if step.tool not in tool_registry:
                    raise ValueError(f"Unknown tool: {step.tool}")
                
                func = tool_registry[step.tool]
                
                # 3. Execute
                print(f"Executing step {i+1}: {step.tool} with {resolved_params}")
                result = func(**resolved_params)
                
                # 4. Store result if requested
                # If result is a dict with 'response' or 'summary' or 'result', prioritize that
                value_to_store = result
                if isinstance(result, dict):
                    if 'summary' in result: value_to_store = result['summary']
                    elif 'response' in result: value_to_store = result['response']
                    elif 'result' in result: value_to_store = result['result']
                
                if step.store_result:
                    variable_name = step.store_result.replace('$', '')
                    self.memory[variable_name] = value_to_store
                
                # IMPORTANT: Set final_result to the unwrapped value (e.g. 12) rather than the dict
                # This makes the workflow return the actual meaningful result
                final_result = value_to_store
                
                execution_log.append({
                    'step': i+1,
                    'tool': step.tool,
                    'status': 'success',
                    'result': str(result)[:100] + '...'
                })
                
            except Exception as e:
                execution_log.append({
                    'step': i+1,
                    'tool': step.tool,
                    'status': 'error',
                    'error': str(e)
                })
                return {
                    'success': False,
                    'message': f"Workflow failed at step {i+1} ({step.tool}): {str(e)}",
                    'log': execution_log
                }
        
        return {
            'success': True,
            'message': 'Workflow completed',
            'result': final_result,
            'log': execution_log
        }
    
    def _resolve_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Substitute variables in parameters.
        Variables look like "$var_name".
        Supports:
        - Exact match: "$result" -> value
        - String interpolation: "Hello $name" -> "Hello World"
        - Arithmetic expressions (via string replacement): "$val + 5" -> "10 + 5"
        """
        resolved = {}
        for k, v in params.items():
            if isinstance(v, str):
                # Check for variables
                if '$' in v:
                    # Case 1: Exact match (e.g., "$result"), preserving type
                    if v.startswith('$') and len(v.split()) == 1:
                        var_name = v[1:]
                        if var_name in self.memory:
                            resolved[k] = self.memory[var_name]
                            continue
                    
                    # Case 2: String interpolation / Expression
                    # We replace all occurrences of $var with its string value
                    new_val = v
                    for var_name, var_val in self.memory.items():
                        # Use backward compatible replacement
                        if f"${var_name}" in new_val:
                            new_val = new_val.replace(f"${var_name}", str(var_val))
                    
                    resolved[k] = new_val
                else:
                    resolved[k] = v
            else:
                resolved[k] = v
        return resolved
