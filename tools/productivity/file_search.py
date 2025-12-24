"""
File Search Tool
Search for files on the system.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import fnmatch


def search_files(
    query: str,
    directory: str = None,
    extensions: List[str] = None,
    max_results: int = 20
) -> Dict[str, any]:
    """
    Search for files by name pattern.
    
    Args:
        query: Search query (supports wildcards like *.pdf)
        directory: Directory to search in (default: user home)
        extensions: List of extensions to filter (e.g., ['.pdf', '.docx'])
        max_results: Maximum number of results
    
    Returns:
        Dictionary with matching files.
    """
    try:
        # Default to user home directory
        if directory is None:
            directory = str(Path.home())
        
        search_path = Path(directory)
        if not search_path.exists():
            return {
                'success': False,
                'message': f'Directory not found: {directory}'
            }
        
        # Prepare query for matching
        query_lower = query.lower()
        
        # If no wildcards, wrap in wildcards
        if '*' not in query and '?' not in query:
            pattern = f'*{query}*'
        else:
            pattern = query
        
        results = []
        
        # Walk through directory
        for root, dirs, files in os.walk(search_path):
            # Skip hidden and system directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', '.git']]
            
            for file in files:
                if len(results) >= max_results:
                    break
                
                # Check if file matches pattern
                if fnmatch.fnmatch(file.lower(), pattern.lower()):
                    # Check extension filter
                    if extensions:
                        ext = Path(file).suffix.lower()
                        if ext not in [e.lower() if e.startswith('.') else f'.{e.lower()}' for e in extensions]:
                            continue
                    
                    filepath = Path(root) / file
                    try:
                        stat = filepath.stat()
                        results.append({
                            'name': file,
                            'path': str(filepath),
                            'size': _format_size(stat.st_size),
                            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                        })
                    except:
                        results.append({
                            'name': file,
                            'path': str(filepath),
                            'size': 'Unknown',
                            'modified': 'Unknown'
                        })
            
            if len(results) >= max_results:
                break
        
        return {
            'success': True,
            'files': results,
            'count': len(results),
            'message': f'Found {len(results)} file(s) matching "{query}"'
        }
        
    except PermissionError:
        return {
            'success': False,
            'message': 'Permission denied accessing some directories'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Search failed: {str(e)}',
            'error': str(e)
        }


def find_recent_files(
    directory: str = None,
    hours: int = 24,
    extensions: List[str] = None,
    max_results: int = 20
) -> Dict[str, any]:
    """
    Find recently modified files.
    
    Args:
        directory: Directory to search (default: user home)
        hours: Find files modified within this many hours
        extensions: Filter by extensions
        max_results: Maximum results
    
    Returns:
        Dictionary with recent files.
    """
    try:
        if directory is None:
            directory = str(Path.home())
        
        search_path = Path(directory)
        cutoff_time = datetime.now() - timedelta(hours=hours)
        cutoff_timestamp = cutoff_time.timestamp()
        
        results = []
        
        for root, dirs, files in os.walk(search_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', '.git']]
            
            for file in files:
                if len(results) >= max_results:
                    break
                
                # Check extension filter
                if extensions:
                    ext = Path(file).suffix.lower()
                    if ext not in [e.lower() if e.startswith('.') else f'.{e.lower()}' for e in extensions]:
                        continue
                
                filepath = Path(root) / file
                try:
                    stat = filepath.stat()
                    if stat.st_mtime >= cutoff_timestamp:
                        results.append({
                            'name': file,
                            'path': str(filepath),
                            'size': _format_size(stat.st_size),
                            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                        })
                except:
                    continue
            
            if len(results) >= max_results:
                break
        
        # Sort by modification time (most recent first)
        results.sort(key=lambda x: x['modified'], reverse=True)
        
        return {
            'success': True,
            'files': results,
            'count': len(results),
            'message': f'Found {len(results)} file(s) modified in the last {hours} hours'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Search failed: {str(e)}',
            'error': str(e)
        }


def find_large_files(
    directory: str = None,
    min_size_mb: int = 100,
    max_results: int = 20
) -> Dict[str, any]:
    """
    Find large files.
    
    Args:
        directory: Directory to search
        min_size_mb: Minimum file size in MB
        max_results: Maximum results
    
    Returns:
        Dictionary with large files.
    """
    try:
        if directory is None:
            directory = str(Path.home())
        
        search_path = Path(directory)
        min_size_bytes = min_size_mb * 1024 * 1024
        
        results = []
        
        for root, dirs, files in os.walk(search_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', '.git']]
            
            for file in files:
                filepath = Path(root) / file
                try:
                    stat = filepath.stat()
                    if stat.st_size >= min_size_bytes:
                        results.append({
                            'name': file,
                            'path': str(filepath),
                            'size': _format_size(stat.st_size),
                            'size_bytes': stat.st_size,
                            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                        })
                except:
                    continue
        
        # Sort by size (largest first)
        results.sort(key=lambda x: x['size_bytes'], reverse=True)
        results = results[:max_results]
        
        # Remove size_bytes from output
        for r in results:
            del r['size_bytes']
        
        return {
            'success': True,
            'files': results,
            'count': len(results),
            'message': f'Found {len(results)} file(s) larger than {min_size_mb}MB'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Search failed: {str(e)}',
            'error': str(e)
        }


def _format_size(size_bytes: int) -> str:
    """Format file size to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f'{size_bytes:.1f} {unit}'
        size_bytes /= 1024
    return f'{size_bytes:.1f} PB'
