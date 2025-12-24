"""
Network Control Tool
Controls WiFi, Bluetooth, and provides network information.
"""

import subprocess
import socket
from typing import Dict, Optional


def get_ip_address() -> Dict[str, any]:
    """
    Get the local IP address.
    
    Returns:
        Dictionary with success status and IP address.
    """
    try:
        # Get local IP by connecting to an external address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        # Also get public IP
        try:
            import requests
            public_ip = requests.get('https://api.ipify.org', timeout=5).text
        except:
            public_ip = 'Could not determine'
        
        return {
            'success': True,
            'local_ip': local_ip,
            'public_ip': public_ip,
            'message': f'Local IP: {local_ip}, Public IP: {public_ip}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to get IP address: {str(e)}',
            'error': str(e)
        }


def toggle_wifi(enable: Optional[bool] = None) -> Dict[str, any]:
    """
    Toggle WiFi on or off.
    
    Args:
        enable: True to enable, False to disable, None to toggle
    
    Returns:
        Dictionary with success status and message.
    """
    try:
        # Get current state if toggling
        if enable is None:
            # Check current state and toggle
            result = subprocess.run(
                ['netsh', 'interface', 'show', 'interface'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            # Look for Wi-Fi adapter status
            if 'Wi-Fi' in result.stdout:
                if 'Disabled' in result.stdout.split('Wi-Fi')[0].split('\n')[-1]:
                    enable = True
                else:
                    enable = False
            else:
                enable = True  # Default to enable if can't determine
        
        action = 'enable' if enable else 'disable'
        
        # Try common WiFi adapter names
        wifi_names = ['Wi-Fi', 'WiFi', 'Wireless Network Connection', 'WLAN']
        
        for name in wifi_names:
            result = subprocess.run(
                ['netsh', 'interface', 'set', 'interface', name, action],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': f'WiFi {"enabled" if enable else "disabled"}',
                    'enabled': enable
                }
        
        return {
            'success': False,
            'message': 'Could not find WiFi adapter. Try running as administrator.'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to toggle WiFi: {str(e)}',
            'error': str(e)
        }


def toggle_bluetooth(enable: Optional[bool] = None) -> Dict[str, any]:
    """
    Toggle Bluetooth on or off.
    
    Args:
        enable: True to enable, False to disable, None to toggle
    
    Returns:
        Dictionary with success status and message.
    """
    try:
        # Bluetooth control on Windows requires PowerShell
        # First check current state
        if enable is None:
            check_cmd = '''
            $bluetooth = Get-PnpDevice | Where-Object { $_.Class -eq "Bluetooth" -and $_.FriendlyName -like "*Bluetooth*" }
            if ($bluetooth) { $bluetooth.Status } else { "NotFound" }
            '''
            result = subprocess.run(
                ['powershell', '-Command', check_cmd],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            current_state = result.stdout.strip()
            enable = current_state != 'OK'
        
        action = 'Enable-PnpDevice' if enable else 'Disable-PnpDevice'
        
        ps_command = f'''
        $bluetooth = Get-PnpDevice | Where-Object {{ $_.Class -eq "Bluetooth" -and $_.FriendlyName -like "*Bluetooth*" }}
        if ($bluetooth) {{
            {action} -InstanceId $bluetooth.InstanceId -Confirm:$false
            "Success"
        }} else {{
            "NotFound"
        }}
        '''
        
        result = subprocess.run(
            ['powershell', '-Command', ps_command],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        if 'Success' in result.stdout:
            return {
                'success': True,
                'message': f'Bluetooth {"enabled" if enable else "disabled"}',
                'enabled': enable
            }
        elif 'NotFound' in result.stdout:
            return {
                'success': False,
                'message': 'Bluetooth adapter not found'
            }
        else:
            return {
                'success': False,
                'message': 'Failed to toggle Bluetooth. Try running as administrator.',
                'output': result.stdout + result.stderr
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to toggle Bluetooth: {str(e)}',
            'error': str(e)
        }


def get_network_info() -> Dict[str, any]:
    """
    Get detailed network information.
    
    Returns:
        Dictionary with network details.
    """
    try:
        result = subprocess.run(
            ['ipconfig', '/all'],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        return {
            'success': True,
            'info': result.stdout,
            'message': 'Network info retrieved'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to get network info: {str(e)}',
            'error': str(e)
        }


def test_internet_connection() -> Dict[str, any]:
    """
    Test if internet connection is available.
    
    Returns:
        Dictionary with connection status.
    """
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return {
            'success': True,
            'connected': True,
            'message': 'Internet connection is active'
        }
    except OSError:
        return {
            'success': True,
            'connected': False,
            'message': 'No internet connection'
        }
