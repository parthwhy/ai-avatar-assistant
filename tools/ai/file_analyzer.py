"""
File Analyzer Tool
Finds and analyzes documents using AI summarization.
Uses the exact code provided by the user.
"""

import os
import requests
from typing import Dict, Any, Optional
from config.settings import settings

# Import PDF libraries
try:
    from pypdf import PdfReader
except ImportError:
    try:
        import PyPDF2
        PdfReader = PyPDF2.PdfReader
    except ImportError:
        PdfReader = None


def find_file(filename_query, search_path):
    """Helper: Finds a file in a specific directory, handling case-insensitivity
    and missing extensions (e.g. finding 'resume.pdf' when looking for 'resume')."""
    if not os.path.exists(search_path):
        return None
    
    query = filename_query.lower()
    query_stem = os.path.splitext(query)[0]
    
    # Store potential matches with priority
    matches = []
    
    for root, dirs, files in os.walk(search_path):
        for file in files:
            file_lower = file.lower()
            file_basename = os.path.splitext(file_lower)[0]
            
            # Priority 1: Exact filename match (e.g. "resume.pdf" == "resume.pdf")
            if query == file_lower:
                return os.path.join(root, file)
            
            # Priority 2: Exact basename match (e.g. "resume" == "resume.pdf")
            if query_stem == file_basename:
                matches.append((1, os.path.join(root, file)))
            
            # Priority 3: Query is contained in filename (e.g. "acceptance" in "acceptance letter.pdf")
            elif query_stem in file_lower:
                matches.append((2, os.path.join(root, file)))
            
            # Priority 4: Filename contains query (e.g. "letter" in "acceptance letter.pdf")
            elif query_stem in file_basename:
                matches.append((3, os.path.join(root, file)))
            
            # Priority 5: Any word from query matches any word in filename
            query_words = query_stem.split()
            file_words = file_basename.replace('-', ' ').replace('_', ' ').split()
            if len(query_words) > 0 and any(qword in file_words for qword in query_words if len(qword) > 2):
                matches.append((4, os.path.join(root, file)))
    
    # Return the best match (lowest priority number)
    if matches:
        matches.sort(key=lambda x: x[0])  # Sort by priority
        return matches[0][1]
    
    return None


def search_across_directories(filename):
    """Helper: Searches current folder, then Desktop, Documents, and Downloads."""
    # 1. Check current folder first
    if os.path.exists(filename):
        return os.path.abspath(filename)
    
    # 2. Define user folders to search
    user_home = os.path.expanduser('~')
    search_paths = [
        os.path.join(user_home, 'Desktop'),
        os.path.join(user_home, 'Documents'),
        os.path.join(user_home, 'Downloads')
    ]
    
    # 3. Search them
    for path in search_paths:
        found_path = find_file(filename, path)
        if found_path:
            return found_path
    
    return None


def extract_text_from_file(file_path):
    """CRITICAL STEP: Opens the file and extracts text so the AI can read it."""
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()
    
    try:
        # Handle PDFs
        if extension == '.pdf':
            if PdfReader is None:
                return "Error: PDF libraries not available. This PDF cannot be read. The file was found but text extraction failed. You may need to install PDF libraries or the PDF might be a scanned image."
            
            reader = PdfReader(file_path)
            if reader.is_encrypted:
                try:
                    reader.decrypt("")
                except:
                    return "Error: PDF is password protected."
            
            text = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
            
            return "\n".join(text) if text else "Error: PDF seems empty or is a scanned image."
        
        # Handle Text files (txt, md, py, csv, etc.)
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
                
    except Exception as e:
        return f"Error reading file: {str(e)}"


def summarize_text(text_content):
    """Sends the text content to Groq Cloud (fast inference) to get a summary."""
    API_KEY = settings.groq_api_key
    
    if not API_KEY:
        return "Error: Missing API Key. Please configure GROQ_API_KEY."
    
    # --- CHANGE 1: CORRECT URL FOR GROQ ---
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # Clean text to avoid JSON errors
    clean_text = text_content.replace('\x00', '')
    if len(clean_text) > 20000:
        clean_text = clean_text[:20000] + "\n...[Truncated]..."
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes documents."
            },
            {
                "role": "user",
                "content": f"Summarize this text:\n\n{clean_text}"
            }
        ],
        # --- CHANGE 2: CORRECT MODEL FOR GROQ ---
        # Groq does not host 'grok-beta'. It hosts Llama 3 and Mixtral.
        "model": "llama-3.1-8b-instant",
        "stream": False,
        "temperature": 0
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"!!! GROQ API ERROR: {response.status_code}")
            print(f"Details: {response.text}")
            return f"AI Error: {response.status_code}"
        
        data = response.json()
        return data['choices'][0]['message']['content']
        
    except Exception as e:
        return f"Connection Error: {str(e)}"


def analyze_document(filename: str) -> Dict[str, Any]:
    """
    Main function to analyze a document by filename.
    
    Args:
        filename: Name of the file to analyze
        
    Returns:
        Dictionary with analysis results
    """
    try:
        print(f"Looking for {filename}...")
        
        # Search for the file
        file_path = search_across_directories(filename)
        
        if not file_path:
            return {
                'success': False,
                'message': f"Sorry, I couldn't find {filename} on your Desktop, Documents, or Downloads.",
                'filename': filename
            }
        
        print(f"Found file at {file_path}. Extracting text...")
        
        # Extract text from the file
        file_content = extract_text_from_file(file_path)
        
        if file_content.startswith("Error"):
            return {
                'success': False,
                'message': f"I found the file, but I couldn't read it. {file_content}",
                'filename': filename,
                'file_path': file_path,
                'error': file_content
            }
        
        print("Analyzing content...")
        
        # Get AI analysis
        analysis_result = summarize_text(file_content)
        
        if analysis_result.startswith("Error") or analysis_result.startswith("AI Error") or analysis_result.startswith("Connection Error"):
            return {
                'success': False,
                'message': f"Found and read the file, but analysis failed: {analysis_result}",
                'filename': filename,
                'file_path': file_path,
                'content_length': len(file_content),
                'error': analysis_result
            }
        
        print("Analysis complete.")
        
        return {
            'success': True,
            'message': f"Successfully analyzed {os.path.basename(file_path)}",
            'filename': filename,
            'file_path': file_path,
            'content_length': len(file_content),
            'analysis': analysis_result,
            'file_size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f"Document analysis error: {str(e)}",
            'filename': filename,
            'error': str(e)
        }