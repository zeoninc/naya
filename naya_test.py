import requests
import json

# Ollama local API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Function to call Ollama's LLaMA 3.2 model
def get_naya_response(prompt):
    payload = {
        "model": "llama3.2",  # Your local LLaMA 3.2 model name in Ollama
        "prompt": prompt,
        "max_tokens": 50,     # Equivalent to max_length in Transformers
        "stream": False       # Get full response, not streamed
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result["response"].strip()
    else:
        return f"Error: API call failed (Status: {response.status_code})"

# Test it
print(get_naya_response("Hello, I am Naya"))