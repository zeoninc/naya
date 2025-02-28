# Replace the existing get_naya_response function in naya_app.py with this
def get_naya_response(prompt, mrn=None):
    base_prompt = "You are Naya, an AI healthcare assistant designed to provide helpful and accurate information with a friendly, professional tone."
    if mrn and mrn in MOCK_PATIENTS:
        patient = MOCK_PATIENTS[mrn]
        context = f"Patient MRN: {mrn}, Name: {patient['name']}, History: {patient['history']}, Labs: {patient['labs']}, Notes: {patient['notes']}."
        full_prompt = f"{base_prompt} {context} User query: {prompt}"
    else:
        full_prompt = f"{base_prompt} User query: {prompt}"

    payload = {
        "model": "llama3.2",  # Updated to LLaMA 3.2
        "prompt": full_prompt,
        "max_tokens": 200,    # Increased for more detailed responses
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            return result["response"].strip()
        else:
            return f"Error: API returned status {response.status_code}"
    except Exception as e:
        return f"Error: Couldn’t connect to Ollama ({str(e)})"