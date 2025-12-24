# System tools module
from .app_launcher import open_app, close_app, type_text, press_key, focus_window
from .brightness import set_brightness, get_brightness, adjust_brightness
from .volume import set_volume, get_volume, mute, unmute, toggle_mute
from .power import lock_screen, sleep, shutdown, restart, schedule_shutdown, cancel_shutdown
from .network import get_ip_address, toggle_wifi, toggle_bluetooth
from .file_search import search_file, open_file_location, search_files_by_type
from .downloads_search import search_downloads
from .text_typer import type_on_screen, type_multiline_text, type_formatted_text, clear_and_type

__all__ = [
    # App launcher
    'open_app', 'close_app', 'type_text', 'press_key', 'focus_window',
    # Brightness
    'set_brightness', 'get_brightness', 'adjust_brightness',
    # Volume
    'set_volume', 'get_volume', 'mute', 'unmute', 'toggle_mute',
    # Power
    'lock_screen', 'sleep', 'shutdown', 'restart', 'schedule_shutdown', 'cancel_shutdown',
    # Network
    'get_ip_address', 'toggle_wifi', 'toggle_bluetooth',
    # File search
    'search_file', 'open_file_location', 'search_files_by_type', 'search_downloads',
    # Text typing
    'type_on_screen', 'type_multiline_text', 'type_formatted_text', 'clear_and_type',
]
