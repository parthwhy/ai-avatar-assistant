"""
System Information Tool
Gets system stats like disk space, battery, and general system info.
"""

import psutil
import platform
import socket
from typing import Dict
from datetime import datetime


def get_disk_space(drive: str = None) -> Dict[str, any]:
    """
    Get disk space information.
    
    Args:
        drive: Specific drive letter (e.g., 'C:') or None for all drives
    
    Returns:
        Dictionary with disk space info.
    """
    try:
        drives_info = []
        
        if drive:
            # Get info for specific drive
            drives = [drive if len(drive) > 1 else f'{drive}:']
        else:
            # Get all drives
            partitions = psutil.disk_partitions()
            drives = [p.mountpoint for p in partitions if 'cdrom' not in p.opts.lower()]
        
        for d in drives:
            try:
                usage = psutil.disk_usage(d)
                drives_info.append({
                    'drive': d,
                    'total': _format_size(usage.total),
                    'used': _format_size(usage.used),
                    'free': _format_size(usage.free),
                    'percent_used': usage.percent
                })
            except:
                continue
        
        if not drives_info:
            return {
                'success': False,
                'message': 'Could not get disk information'
            }
        
        # Create summary message
        if len(drives_info) == 1:
            d = drives_info[0]
            message = f"{d['drive']} - {d['free']} free of {d['total']} ({100-d['percent_used']:.1f}% available)"
        else:
            message = f"Found {len(drives_info)} drives"
        
        return {
            'success': True,
            'drives': drives_info,
            'message': message
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to get disk space: {str(e)}',
            'error': str(e)
        }


def get_system_info() -> Dict[str, any]:
    """
    Get general system information.
    
    Returns:
        Dictionary with system info.
    """
    try:
        # CPU info
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        # Memory info
        memory = psutil.virtual_memory()
        
        # System info
        uname = platform.uname()
        
        # Boot time
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        info = {
            'system': uname.system,
            'node_name': uname.node,
            'release': uname.release,
            'version': uname.version,
            'machine': uname.machine,
            'processor': uname.processor,
            'cpu_cores': cpu_count,
            'cpu_frequency_mhz': round(cpu_freq.current) if cpu_freq else 'Unknown',
            'cpu_usage_percent': cpu_percent,
            'memory_total': _format_size(memory.total),
            'memory_used': _format_size(memory.used),
            'memory_available': _format_size(memory.available),
            'memory_percent': memory.percent,
            'boot_time': boot_time.strftime('%Y-%m-%d %H:%M:%S'),
            'uptime': str(uptime).split('.')[0]  # Remove microseconds
        }
        
        return {
            'success': True,
            'info': info,
            'message': f'{uname.system} {uname.release} | CPU: {cpu_percent}% | RAM: {memory.percent}% used'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to get system info: {str(e)}',
            'error': str(e)
        }


def get_battery_status() -> Dict[str, any]:
    """
    Get battery status (for laptops).
    
    Returns:
        Dictionary with battery info.
    """
    try:
        battery = psutil.sensors_battery()
        
        if battery is None:
            return {
                'success': True,
                'has_battery': False,
                'message': 'No battery detected (desktop PC)'
            }
        
        # Calculate time remaining
        if battery.secsleft == psutil.POWER_TIME_UNLIMITED:
            time_remaining = 'Charging'
        elif battery.secsleft == psutil.POWER_TIME_UNKNOWN:
            time_remaining = 'Unknown'
        else:
            hours = battery.secsleft // 3600
            minutes = (battery.secsleft % 3600) // 60
            time_remaining = f'{hours}h {minutes}m'
        
        status = 'Charging' if battery.power_plugged else 'Discharging'
        
        return {
            'success': True,
            'has_battery': True,
            'percent': battery.percent,
            'plugged_in': battery.power_plugged,
            'status': status,
            'time_remaining': time_remaining,
            'message': f'Battery: {battery.percent}% ({status}) - {time_remaining}'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to get battery status: {str(e)}',
            'error': str(e)
        }


def get_running_processes(top_n: int = 10) -> Dict[str, any]:
    """
    Get top processes by CPU/memory usage.
    
    Args:
        top_n: Number of top processes to return
    
    Returns:
        Dictionary with process list.
    """
    try:
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                pinfo = proc.info
                processes.append({
                    'pid': pinfo['pid'],
                    'name': pinfo['name'],
                    'cpu_percent': pinfo['cpu_percent'] or 0,
                    'memory_percent': round(pinfo['memory_percent'] or 0, 2)
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by CPU + memory usage
        processes.sort(key=lambda x: x['cpu_percent'] + x['memory_percent'], reverse=True)
        top_processes = processes[:top_n]
        
        return {
            'success': True,
            'processes': top_processes,
            'count': len(top_processes),
            'message': f'Top {len(top_processes)} processes by resource usage'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to get processes: {str(e)}',
            'error': str(e)
        }


def _format_size(size_bytes: int) -> str:
    """Format bytes to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f'{size_bytes:.1f} {unit}'
        size_bytes /= 1024
    return f'{size_bytes:.1f} PB'
