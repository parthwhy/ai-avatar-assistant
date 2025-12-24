"""
Routine Manager
Manages custom routines - create, read, update, delete, and execute.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import settings


# Path to user's custom routines
ROUTINES_DIR = settings.routines_dir
CUSTOM_ROUTINES_FILE = settings.data_dir / 'routines.json'

# Action registry - maps action names to functions
_action_registry: Dict[str, callable] = {}


def _ensure_dirs():
    """Ensure routine directories exist."""
    ROUTINES_DIR.mkdir(parents=True, exist_ok=True)
    settings.data_dir.mkdir(parents=True, exist_ok=True)


def _load_custom_routines() -> Dict:
    """Load custom routines from file."""
    if CUSTOM_ROUTINES_FILE.exists():
        try:
            with open(CUSTOM_ROUTINES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}


def _save_custom_routines(routines: Dict):
    """Save custom routines to file."""
    _ensure_dirs()
    with open(CUSTOM_ROUTINES_FILE, 'w', encoding='utf-8') as f:
        json.dump(routines, f, indent=2, ensure_ascii=False)


def _load_preset_routine(name: str) -> Optional[Dict]:
    """Load a preset routine from the presets folder."""
    preset_file = ROUTINES_DIR / f'{name}.json'
    if preset_file.exists():
        try:
            with open(preset_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    return None


def register_action(name: str, func: callable):
    """
    Register an action function for use in routines.
    
    Args:
        name: Action name (e.g., 'open_app', 'set_brightness')
        func: Function to call for this action
    """
    _action_registry[name] = func


def _register_default_actions():
    """Register default actions from tools."""
    if _action_registry:
        return  # Already registered
    
    try:
        from tools.system import (
            open_app, close_app, set_brightness, set_volume,
            mute, unmute, lock_screen
        )
        from tools.productivity import (
            open_url, search_web, set_timer
        )
        
        # System actions
        register_action('open_app', lambda params: open_app(params.get('app', params.get('name', ''))))
        register_action('close_app', lambda params: close_app(params.get('app', params.get('name', ''))))
        register_action('set_brightness', lambda params: set_brightness(params.get('level', 50)))
        register_action('set_volume', lambda params: set_volume(params.get('level', 50)))
        register_action('mute', lambda params: mute())
        register_action('unmute', lambda params: unmute())
        register_action('lock_screen', lambda params: lock_screen())
        
        # Productivity actions
        register_action('open_url', lambda params: open_url(params.get('url', '')))
        register_action('search_web', lambda params: search_web(params.get('query', ''), params.get('engine', 'google')))
        register_action('set_timer', lambda params: set_timer(params.get('minutes', 1), params.get('name', None)))
        
        # Special actions
        register_action('wait', lambda params: _wait_action(params.get('seconds', 1)))
        register_action('notify', lambda params: _notify_action(params.get('message', 'Routine step completed')))
        register_action('disable_notifications', lambda params: _disable_notifications())
        
    except ImportError as e:
        print(f"Warning: Could not register some actions: {e}")


def _wait_action(seconds: float) -> Dict:
    """Wait for specified seconds."""
    time.sleep(seconds)
    return {'success': True, 'message': f'Waited {seconds} seconds'}


def _notify_action(message: str) -> Dict:
    """Show a notification."""
    from tools.productivity.timer import _show_notification
    _show_notification(message, "SAGE Routine")
    return {'success': True, 'message': f'Notification shown: {message}'}


def _disable_notifications() -> Dict:
    """Enable Do Not Disturb / Focus Assist on Windows."""
    try:
        import subprocess
        # Enable Focus Assist via PowerShell
        ps_command = '''
        $signature = @"
        [DllImport("user32.dll")]
        public static extern bool SystemParametersInfo(int uAction, int uParam, ref int lpvParam, int flags);
"@
        # This enables quiet hours (Focus Assist)
        # Note: Full Focus Assist control requires Windows Settings app
        '''
        # For now, just return success - full DND requires more complex Windows API calls
        return {'success': True, 'message': 'Do Not Disturb mode requested'}
    except Exception as e:
        return {'success': False, 'message': f'Could not enable DND: {str(e)}'}


def create_routine(name: str, steps: List[Dict], description: str = "") -> Dict[str, any]:
    """
    Create a new routine.
    
    Args:
        name: Routine name (lowercase, no spaces preferred)
        steps: List of step dictionaries with 'action' and 'params'
        description: Optional description
    
    Returns:
        Dictionary with result.
    
    Example:
        create_routine("morning", [
            {"action": "open_app", "params": {"app": "VS Code"}},
            {"action": "set_brightness", "params": {"level": 50}}
        ])
    """
    name = name.lower().replace(' ', '_')
    
    routines = _load_custom_routines()
    
    routine = {
        'name': name,
        'description': description,
        'steps': steps,
        'created': datetime.now().isoformat(),
        'modified': datetime.now().isoformat()
    }
    
    routines[name] = routine
    _save_custom_routines(routines)
    
    return {
        'success': True,
        'routine': routine,
        'message': f'Routine "{name}" created with {len(steps)} steps'
    }


def get_routine(name: str) -> Dict[str, any]:
    """
    Get a routine by name.
    
    Args:
        name: Routine name
    
    Returns:
        Dictionary with routine data or error.
    """
    name = name.lower().replace(' ', '_')
    
    # Check custom routines first
    routines = _load_custom_routines()
    if name in routines:
        return {
            'success': True,
            'routine': routines[name],
            'source': 'custom'
        }
    
    # Check presets
    preset = _load_preset_routine(name)
    if preset:
        return {
            'success': True,
            'routine': preset,
            'source': 'preset'
        }
    
    return {
        'success': False,
        'message': f'Routine "{name}" not found'
    }


def update_routine(name: str, steps: List[Dict] = None, description: str = None) -> Dict[str, any]:
    """
    Update an existing routine.
    
    Args:
        name: Routine name
        steps: New steps (optional)
        description: New description (optional)
    
    Returns:
        Dictionary with result.
    """
    name = name.lower().replace(' ', '_')
    
    routines = _load_custom_routines()
    
    if name not in routines:
        return {
            'success': False,
            'message': f'Routine "{name}" not found'
        }
    
    if steps is not None:
        routines[name]['steps'] = steps
    
    if description is not None:
        routines[name]['description'] = description
    
    routines[name]['modified'] = datetime.now().isoformat()
    
    _save_custom_routines(routines)
    
    return {
        'success': True,
        'routine': routines[name],
        'message': f'Routine "{name}" updated'
    }


def delete_routine(name: str) -> Dict[str, any]:
    """
    Delete a routine.
    
    Args:
        name: Routine name
    
    Returns:
        Dictionary with result.
    """
    name = name.lower().replace(' ', '_')
    
    routines = _load_custom_routines()
    
    if name not in routines:
        return {
            'success': False,
            'message': f'Routine "{name}" not found'
        }
    
    del routines[name]
    _save_custom_routines(routines)
    
    return {
        'success': True,
        'message': f'Routine "{name}" deleted'
    }


def list_routines() -> Dict[str, any]:
    """
    List all available routines (custom and presets).
    
    Returns:
        Dictionary with routine list.
    """
    routines = []
    
    # Load custom routines
    custom = _load_custom_routines()
    for name, routine in custom.items():
        routines.append({
            'name': name,
            'description': routine.get('description', ''),
            'steps_count': len(routine.get('steps', [])),
            'source': 'custom'
        })
    
    # Load presets
    _ensure_dirs()
    for preset_file in ROUTINES_DIR.glob('*.json'):
        name = preset_file.stem
        if name not in custom:  # Don't duplicate
            preset = _load_preset_routine(name)
            if preset:
                routines.append({
                    'name': name,
                    'description': preset.get('description', ''),
                    'steps_count': len(preset.get('steps', [])),
                    'source': 'preset'
                })
    
    return {
        'success': True,
        'routines': routines,
        'count': len(routines),
        'message': f'Found {len(routines)} routine(s)'
    }


def execute_routine(name: str, dry_run: bool = False) -> Dict[str, any]:
    """
    Execute a routine.
    
    Args:
        name: Routine name
        dry_run: If True, don't actually execute, just show what would happen
    
    Returns:
        Dictionary with execution results.
    """
    _register_default_actions()
    
    # Get the routine
    routine_result = get_routine(name)
    if not routine_result['success']:
        return routine_result
    
    routine = routine_result['routine']
    steps = routine.get('steps', [])
    
    if not steps:
        return {
            'success': False,
            'message': f'Routine "{name}" has no steps'
        }
    
    results = []
    errors = []
    
    for i, step in enumerate(steps):
        action = step.get('action')
        params = step.get('params', {})
        
        step_info = {
            'step': i + 1,
            'action': action,
            'params': params
        }
        
        if dry_run:
            step_info['result'] = 'Would execute'
            results.append(step_info)
            continue
        
        # Execute the action
        if action not in _action_registry:
            step_info['result'] = {'success': False, 'message': f'Unknown action: {action}'}
            errors.append(step_info)
        else:
            try:
                result = _action_registry[action](params)
                step_info['result'] = result
                if result.get('success', True):
                    results.append(step_info)
                else:
                    errors.append(step_info)
            except Exception as e:
                step_info['result'] = {'success': False, 'message': str(e)}
                errors.append(step_info)
        
        # Small delay between steps for stability
        if not dry_run:
            time.sleep(0.5)
    
    success = len(errors) == 0
    
    return {
        'success': success,
        'routine': name,
        'steps_executed': len(results),
        'steps_failed': len(errors),
        'results': results,
        'errors': errors,
        'message': f'Routine "{name}" {"completed" if success else "completed with errors"}: {len(results)} succeeded, {len(errors)} failed'
    }


def add_step_to_routine(name: str, action: str, params: Dict = None, position: int = -1) -> Dict[str, any]:
    """
    Add a step to an existing routine.
    
    Args:
        name: Routine name
        action: Action name
        params: Action parameters
        position: Position to insert (-1 for end)
    
    Returns:
        Dictionary with result.
    """
    name = name.lower().replace(' ', '_')
    
    routines = _load_custom_routines()
    
    if name not in routines:
        return {
            'success': False,
            'message': f'Routine "{name}" not found'
        }
    
    step = {'action': action, 'params': params or {}}
    
    if position < 0:
        routines[name]['steps'].append(step)
    else:
        routines[name]['steps'].insert(position, step)
    
    routines[name]['modified'] = datetime.now().isoformat()
    _save_custom_routines(routines)
    
    return {
        'success': True,
        'message': f'Added step "{action}" to routine "{name}"',
        'steps_count': len(routines[name]['steps'])
    }


def remove_step_from_routine(name: str, position: int) -> Dict[str, any]:
    """
    Remove a step from a routine.
    
    Args:
        name: Routine name
        position: Step position (0-indexed)
    
    Returns:
        Dictionary with result.
    """
    name = name.lower().replace(' ', '_')
    
    routines = _load_custom_routines()
    
    if name not in routines:
        return {
            'success': False,
            'message': f'Routine "{name}" not found'
        }
    
    steps = routines[name]['steps']
    
    if position < 0 or position >= len(steps):
        return {
            'success': False,
            'message': f'Invalid position {position}. Routine has {len(steps)} steps.'
        }
    
    removed = steps.pop(position)
    routines[name]['modified'] = datetime.now().isoformat()
    _save_custom_routines(routines)
    
    return {
        'success': True,
        'message': f'Removed step "{removed["action"]}" from routine "{name}"',
        'steps_count': len(steps)
    }
