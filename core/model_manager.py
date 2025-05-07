import requests

def list_available_models():
    """
    Queries the Ollama API to list all available models.
    """
    try:
        response = requests.get("http://localhost:11434/api/models")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"] for model in models]
        else:
            return ["mistral"]
    except requests.exceptions.RequestException:
        return []

def query_ollama(prompt, model="mistral"):
    """
    Queries the selected model (Mistral or LLaMA) through the Ollama API.
    """
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        if response.status_code == 200:
            return response.json().get("response", "No response from LLM.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error contacting Ollama API: {str(e)}"
