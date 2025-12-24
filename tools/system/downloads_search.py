"""
Downloads Folder Search Tool
Focused search only in Downloads folder with GUI options to open files.
"""

import os
import glob
import subprocess
import tkinter as tk
from tkinter import messagebox
from typing import List, Dict, Any


def search_downloads(filename: str) -> Dict[str, Any]:
    """
    Search for files only in the Downloads folder.
    
    Args:
        filename: Name or partial name of the file to search for
        
    Returns:
        Dictionary with search results and GUI options
    """
    try:
        downloads_path = os.path.expanduser("~/Downloads")
        
        if not os.path.exists(downloads_path):
            return {
                'success': False,
                'message': 'Downloads folder not found'
            }
        
        # Clean filename for search
        filename = filename.strip()
        if not filename:
            return {
                'success': False,
                'message': 'Please provide a filename to search for'
            }
        
        found_files = []
        
        # Search patterns in Downloads folder only
        patterns = [
            f"*{filename}*",      # Contains filename
            f"{filename}",        # Exact match
            f"{filename}.*",      # With any extension
        ]
        
        for pattern in patterns:
            search_pattern = os.path.join(downloads_path, pattern)
            matches = glob.glob(search_pattern)
            
            for match in matches:
                if os.path.exists(match) and match not in found_files:
                    found_files.append(match)
        
        # Also search in subdirectories
        for pattern in patterns:
            search_pattern = os.path.join(downloads_path, "**", pattern)
            matches = glob.glob(search_pattern, recursive=True)
            
            for match in matches:
                if os.path.exists(match) and match not in found_files:
                    found_files.append(match)
        
        # Sort by modification time (newest first)
        found_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        # Take only top 10 results
        found_files = found_files[:10]
        
        # Format results
        results = []
        for filepath in found_files:
            try:
                stat = os.stat(filepath)
                size = stat.st_size
                
                # Format file size
                if size < 1024:
                    size_str = f"{size} bytes"
                elif size < 1024 * 1024:
                    size_str = f"{size // 1024} KB"
                else:
                    size_str = f"{size // (1024 * 1024)} MB"
                
                # Determine file type
                if os.path.isdir(filepath):
                    file_type = "Folder"
                    size_str = f"{len(os.listdir(filepath))} items" if os.access(filepath, os.R_OK) else "Folder"
                else:
                    file_type = "File"
                
                results.append({
                    'path': filepath,
                    'name': os.path.basename(filepath),
                    'type': file_type,
                    'size': size_str,
                    'modified': os.path.getmtime(filepath)
                })
                
            except (OSError, PermissionError):
                results.append({
                    'path': filepath,
                    'name': os.path.basename(filepath),
                    'type': "Unknown",
                    'size': "Unknown",
                    'modified': 0
                })
        
        if results:
            # Show GUI for top 2 results if more than 0 found
            if len(results) >= 1:
                show_downloads_gui(results[:2], filename)
            
            message = f"Found {len(results)} result{'s' if len(results) != 1 else ''} in Downloads for '{filename}'"
            return {
                'success': True,
                'message': message,
                'results': results,
                'count': len(results),
                'gui_shown': len(results) >= 1
            }
        else:
            return {
                'success': False,
                'message': f"No files found in Downloads matching '{filename}'",
                'results': [],
                'count': 0
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f"Downloads search error: {str(e)}",
            'results': [],
            'count': 0
        }


def show_downloads_gui(results: List[Dict[str, Any]], search_term: str):
    """
    Show GUI with top 2 results and clickable options to open them.
    
    Args:
        results: List of file results (max 2)
        search_term: Original search term
    """
    try:
        # Create popup window
        popup = tk.Toplevel()
        popup.title(f"Downloads Search: {search_term}")
        popup.geometry("400x200")
        popup.configure(bg="#2d2d2d")
        popup.attributes("-topmost", True)
        
        # Center the window
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (400 // 2)
        y = (popup.winfo_screenheight() // 2) - (200 // 2)
        popup.geometry(f"400x200+{x}+{y}")
        
        # Title
        title_label = tk.Label(
            popup, 
            text=f"Found in Downloads: {search_term}",
            fg="#ffffff",
            bg="#2d2d2d",
            font=("Arial", 12, "bold")
        )
        title_label.pack(pady=10)
        
        # Results frame
        results_frame = tk.Frame(popup, bg="#2d2d2d")
        results_frame.pack(fill="both", expand=True, padx=20)
        
        for i, result in enumerate(results[:2], 1):
            # File info frame
            file_frame = tk.Frame(results_frame, bg="#3d3d3d", relief="raised", bd=1)
            file_frame.pack(fill="x", pady=5)
            
            # File name and info
            name_label = tk.Label(
                file_frame,
                text=f"{i}. {result['name']}",
                fg="#00ff88",
                bg="#3d3d3d",
                font=("Arial", 10, "bold"),
                anchor="w"
            )
            name_label.pack(fill="x", padx=10, pady=(5, 0))
            
            info_label = tk.Label(
                file_frame,
                text=f"{result['type']} • {result['size']}",
                fg="#cccccc",
                bg="#3d3d3d",
                font=("Arial", 8),
                anchor="w"
            )
            info_label.pack(fill="x", padx=10, pady=(0, 5))
            
            # Open button
            open_btn = tk.Button(
                file_frame,
                text="📂 Open",
                command=lambda path=result['path']: open_file_or_folder(path, popup),
                bg="#4CAF50",
                fg="white",
                font=("Arial", 9),
                cursor="hand2",
                relief="flat"
            )
            open_btn.pack(side="right", padx=10, pady=5)
        
        # Close button
        close_btn = tk.Button(
            popup,
            text="Close",
            command=popup.destroy,
            bg="#666666",
            fg="white",
            font=("Arial", 9),
            cursor="hand2",
            relief="flat"
        )
        close_btn.pack(pady=10)
        
        # Auto-close after 30 seconds
        popup.after(30000, popup.destroy)
        
    except Exception as e:
        print(f"GUI Error: {e}")


def open_file_or_folder(filepath: str, popup_window: tk.Toplevel = None):
    """
    Open file or folder and close the popup.
    
    Args:
        filepath: Path to file or folder to open
        popup_window: Popup window to close after opening
    """
    try:
        if os.path.isdir(filepath):
            # Open folder
            subprocess.run(['explorer', filepath], check=True)
            message = f"Opened folder: {os.path.basename(filepath)}"
        else:
            # Open file with default application
            subprocess.run(['start', '', filepath], shell=True, check=True)
            message = f"Opened file: {os.path.basename(filepath)}"
        
        print(f"✅ {message}")
        
        # Close popup if provided
        if popup_window:
            popup_window.destroy()
            
        return {
            'success': True,
            'message': message
        }
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to open {os.path.basename(filepath)}: {str(e)}"
        print(f"❌ {error_msg}")
        
        if popup_window:
            messagebox.showerror("Error", error_msg)
        
        return {
            'success': False,
            'message': error_msg
        }
    except Exception as e:
        error_msg = f"Error opening {os.path.basename(filepath)}: {str(e)}"
        print(f"❌ {error_msg}")
        
        if popup_window:
            messagebox.showerror("Error", error_msg)
        
        return {
            'success': False,
            'message': error_msg
        }