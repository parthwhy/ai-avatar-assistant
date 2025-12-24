"""
Brain Logic (Now powered by Groq/Llama 3)
Handles AI interactions for SAGE.
"""

import os
from groq import Groq
from config.settings import settings

class Brain:
    """
    Intelligence layer using Groq API.
    Fast, reliable, and generous limits.
    """
    
    def __init__(self):
        key = settings.groq_api_key
        if not key:
            print("Warning: GROQ_API_KEY not found.")
            self.client = None
        else:
            self.client = Groq(api_key=key)
            
        # Llama 3.3 70B is the current stable production model
        self.model = "llama-3.3-70b-versatile"

    def ask(self, prompt: str) -> str:
        """Simple query."""
        if not self.client: return "I don't have a brain (API Key missing)."
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are SAGE, a helpful desktop assistant. Keep responses concise and plain text."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Brain Error: {e}")
            return "I had a headache (API Error)."

    def chat(self, user_message: str, history: list = None) -> str:
        """Conversational query."""
        if not self.client: return "Brain offline."
        
        messages = [
             {"role": "system", "content": "You are SAGE, a helpful AI assistant. Be concise."}
        ]
        
        if history:
            messages.extend(history)
            
        messages.append({"role": "user", "content": user_message})
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

    def analyze_intent(self, text: str) -> dict:
        """
        Determine intent from text.
        Returns JSON structure.
        """
        if not self.client: return {"type": "unknown"}
        
        prompt = f"""
        Analyze this command: "{text}"
        Return JSON ONLY.
        Format: {{ "intent": "command_name", "params": {{ "param1": "value" }} }}
        
        Known intents:
        - open_app (app)
        - set_volume (level)
        - set_brightness (level)
        - get_weather (city)
        - web_search (query)
        - general_query (if none match)
        """
        
        try:
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a JSON parser. Output only JSON."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                response_format={"type": "json_object"}
            )
            raw_content = completion.choices[0].message.content
            
            import json
            # Sanitize potential markdown
            cleaned_content = raw_content.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned_content)
        except Exception as e:
            print(f"[DEBUG] Intent Analysis Failed: {e}")
            return {"intent": "general_query", "query": text}

# Global instance
_brain = None

def get_brain():
    global _brain
    if _brain is None:
        _brain = Brain()
    return _brain

# Wrapper functions for core.__init__ compatibility
def ask(prompt: str) -> str:
    return get_brain().ask(prompt)

def chat(message: str, history: list = None) -> str:
    return get_brain().chat(message, history)
