"""
Task Executor - Agentic Version
Uses the new Orchestrator Agent for intelligent tool calling and multi-step workflows.
"""

from typing import Dict, Any
from .orchestrator import get_orchestrator

class TaskExecutor:
    """
    Central hub for executing user requests using the agentic orchestrator.
    """
    
    def __init__(self):
        self.orchestrator = get_orchestrator()
        
    def execute(self, user_input: str) -> Dict[str, Any]:
        """
        Execute a user request using the orchestrator agent.
        
        Args:
            user_input: Natural language command
            
        Returns:
            Execution result
        """
        # Use the orchestrator for all requests
        result = self.orchestrator.orchestrate(user_input)
        
        # Format the response for backward compatibility
        if result['success']:
            if result.get('tool_calls'):
                # Tool execution result
                return {
                    'success': True,
                    'type': 'agentic',
                    'thinking': result.get('thinking', ''),
                    'tool_calls': result['tool_calls'],
                    'execution_log': result.get('execution_log', []),
                    'message': self._format_execution_summary(result)
                }
            else:
                # Conversation result
                return {
                    'success': True,
                    'type': 'conversation',
                    'response': result.get('response', 'No response'),
                    'thinking': result.get('thinking', '')
                }
        else:
            # Error result
            return result
    
    def _format_execution_summary(self, result: Dict[str, Any]) -> str:
        """Format a summary of tool executions for user feedback."""
        if not result.get('tool_calls'):
            return result.get('response', 'Task completed')
        
        successful_tools = []
        failed_tools = []
        
        for log_entry in result.get('execution_log', []):
            if log_entry['status'] == 'success':
                successful_tools.append(log_entry['tool'])
            else:
                failed_tools.append(log_entry['tool'])
        
        summary_parts = []
        
        if successful_tools:
            summary_parts.append(f"✅ Executed: {', '.join(successful_tools)}")
        
        if failed_tools:
            summary_parts.append(f"❌ Failed: {', '.join(failed_tools)}")
        
        if result.get('response'):
            summary_parts.append(result['response'])
        
        return ' | '.join(summary_parts) if summary_parts else 'Task completed'


# Global instance
_executor = None

def get_executor() -> TaskExecutor:
    global _executor
    if _executor is None:
        _executor = TaskExecutor()
    return _executor
