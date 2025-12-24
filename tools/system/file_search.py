"""
File Search Tool
Search for files and folders on the system using Windows search capabilities.
"""

import os
import glob
import subprocess
import time
from typing import List, Dict, Any


def search_file(filename: str, search_path: str = None, max_results: int = 10) -> Dict[str, Any]:
    """
    Search for files by name on the system.
    
    Args:
        filename: Name or partial name of the file to search for
        search_path: Optional path to search in (defaults to common locations)
        max_results: Maximum number of results to return
        
    Returns:
        Dictionary with search results
    """
    try:
        results = []
        
        # Clean filename for search
        filename = filename.strip()
        if not filename:
            return {
                'success': False,
                'message': 'Please provide a filename to search for'
            }
        
        # If no specific path provided, search in common locations
        if not search_path:
            search_paths = [
                os.path.expanduser("~"),  # User home directory
                "C:\\Users",  # All users
                "C:\\Program Files",  # Program files
                "C:\\Program Files (x86)",  # 32-bit programs
                "D:\\" if os.path.exists("D:\\") else None,  # D drive if exists
            ]
            search_paths = [p for p in search_paths if p and os.path.exists(p)]
        else:
            search_paths = [search_path]
        
        # Search using different methods
        found_files = []
        
        # Method 1: Use glob pattern matching
        for base_path in search_paths:
            try:
                # Search for exact matches and partial matches
                patterns = [
                    f"**/*{filename}*",  # Contains filename
                    f"**/{filename}",    # Exact match
                    f"**/{filename}.*",  # With any extension
                ]
                
                for pattern in patterns:
                    search_pattern = os.path.join(base_path, pattern)
                    matches = glob.glob(search_pattern, recursive=True)
                    
                    for match in matches[:max_results]:
                        if os.path.exists(match) and match not in found_files:
                            found_files.append(match)
                            
                            if len(found_files) >= max_results:
                                break
                    
                    if len(found_files) >= max_results:
                        break
                        
            except (PermissionError, OSError):
                continue  # Skip inaccessible directories
            
            if len(found_files) >= max_results:
                break
        
        # Method 2: Try Windows search command if glob didn't find much
        if len(found_files) < 3:
            try:
                # Use Windows 'where' command for executables
                if not filename.endswith(('.txt', '.doc', '.pdf', '.jpg', '.png')):
                    result = subprocess.run(
                        ['where', filename],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        for line in result.stdout.strip().split('\n'):
                            if line.strip() and line not in found_files:
                                found_files.append(line.strip())
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
        
        # Format results
        for filepath in found_files[:max_results]:
            try:
                stat = os.stat(filepath)
                size = stat.st_size
                modified = time.ctime(stat.st_mtime)
                
                # Determine file type
                if os.path.isdir(filepath):
                    file_type = "Folder"
                    size_str = f"{len(os.listdir(filepath))} items" if os.access(filepath, os.R_OK) else "Folder"
                else:
                    file_type = "File"
                    if size < 1024:
                        size_str = f"{size} bytes"
                    elif size < 1024 * 1024:
                        size_str = f"{size // 1024} KB"
                    else:
                        size_str = f"{size // (1024 * 1024)} MB"
                
                results.append({
                    'path': filepath,
                    'name': os.path.basename(filepath),
                    'type': file_type,
                    'size': size_str,
                    'modified': modified,
                    'directory': os.path.dirname(filepath)
                })
                
            except (OSError, PermissionError):
                # Add basic info if we can't get stats
                results.append({
                    'path': filepath,
                    'name': os.path.basename(filepath),
                    'type': "File" if os.path.isfile(filepath) else "Folder",
                    'size': "Unknown",
                    'modified': "Unknown",
                    'directory': os.path.dirname(filepath)
                })
        
        if results:
            message = f"Found {len(results)} result{'s' if len(results) != 1 else ''} for '{filename}'"
            return {
                'success': True,
                'message': message,
                'results': results,
                'count': len(results)
            }
        else:
            return {
                'success': False,
                'message': f"No files found matching '{filename}'",
                'results': [],
                'count': 0
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f"Search error: {str(e)}",
            'results': [],
            'count': 0
        }


def open_file_location(filepath: str) -> Dict[str, Any]:
    """
    Open the folder containing the specified file.
    
    Args:
        filepath: Full path to the file
        
    Returns:
        Dictionary with operation result
    """
    try:
        if not os.path.exists(filepath):
            return {
                'success': False,
                'message': f"File not found: {filepath}"
            }
        
        # Open folder and select the file
        subprocess.run(['explorer', '/select,', filepath], check=True)
        
        return {
            'success': True,
            'message': f"Opened location of {os.path.basename(filepath)}"
        }
        
    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'message': f"Failed to open file location: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'message': f"Error opening file location: {str(e)}"
        }


def search_files_by_type(file_type: str, search_path: str = None, max_results: int = 10) -> Dict[str, Any]:
    """
    Search for files by type/extension.
    
    Args:
        file_type: File type to search for (e.g., 'pdf', 'image', 'document')
        search_path: Optional path to search in
        max_results: Maximum number of results to return
        
    Returns:
        Dictionary with search results
    """
    try:
        # Map file types to extensions
        type_extensions = {
            'document': ['*.doc', '*.docx', '*.pdf', '*.txt', '*.rtf'],
            'image': ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff'],
            'video': ['*.mp4', '*.avi', '*.mkv', '*.mov', '*.wmv', '*.flv'],
            'audio': ['*.mp3', '*.wav', '*.flac', '*.aac', '*.ogg', '*.wma'],
            'spreadsheet': ['*.xls', '*.xlsx', '*.csv'],
            'presentation': ['*.ppt', '*.pptx'],
            'archive': ['*.zip', '*.rar', '*.7z', '*.tar', '*.gz'],
            'executable': ['*.exe', '*.msi', '*.bat', '*.cmd']
        }
        
        # Get extensions for the requested type
        if file_type.lower() in type_extensions:
            extensions = type_extensions[file_type.lower()]
        elif file_type.startswith('.'):
            extensions = [f"*{file_type}"]
        else:
            extensions = [f"*.{file_type}"]
        
        # Search paths
        if not search_path:
            search_paths = [
                os.path.expanduser("~/Documents"),
                os.path.expanduser("~/Downloads"),
                os.path.expanduser("~/Desktop"),
                os.path.expanduser("~/Pictures"),
                os.path.expanduser("~/Videos"),
                os.path.expanduser("~/Music"),
            ]
            search_paths = [p for p in search_paths if os.path.exists(p)]
        else:
            search_paths = [search_path]
        
        found_files = []
        
        for base_path in search_paths:
            for extension in extensions:
                try:
                    pattern = os.path.join(base_path, "**", extension)
                    matches = glob.glob(pattern, recursive=True)
                    
                    for match in matches:
                        if os.path.isfile(match) and match not in found_files:
                            found_files.append(match)
                            
                        if len(found_files) >= max_results:
                            break
                            
                except (PermissionError, OSError):
                    continue
                
                if len(found_files) >= max_results:
                    break
            
            if len(found_files) >= max_results:
                break
        
        # Format results
        results = []
        for filepath in found_files[:max_results]:
            try:
                stat = os.stat(filepath)
                size = stat.st_size
                modified = time.ctime(stat.st_mtime)
                
                if size < 1024:
                    size_str = f"{size} bytes"
                elif size < 1024 * 1024:
                    size_str = f"{size // 1024} KB"
                else:
                    size_str = f"{size // (1024 * 1024)} MB"
                
                results.append({
                    'path': filepath,
                    'name': os.path.basename(filepath),
                    'type': file_type.title(),
                    'size': size_str,
                    'modified': modified,
                    'directory': os.path.dirname(filepath)
                })
                
            except (OSError, PermissionError):
                results.append({
                    'path': filepath,
                    'name': os.path.basename(filepath),
                    'type': file_type.title(),
                    'size': "Unknown",
                    'modified': "Unknown",
                    'directory': os.path.dirname(filepath)
                })
        
        if results:
            message = f"Found {len(results)} {file_type} file{'s' if len(results) != 1 else ''}"
            return {
                'success': True,
                'message': message,
                'results': results,
                'count': len(results)
            }
        else:
            return {
                'success': False,
                'message': f"No {file_type} files found",
                'results': [],
                'count': 0
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f"Search error: {str(e)}",
            'results': [],
            'count': 0
        }