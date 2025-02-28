from transformers import pipeline

# Load model (use distilgpt2 for now, swap with Llama-2-7b-hf later)
generator = pipeline("text-generation", model="distilgpt2")

def get_naya_response(user_input):
    prompt = f"You are Naya, an AI healthcare assistant designed to provide helpful and accurate information with a friendly, professional tone. User query: {user_input}"
    response = generator(prompt, max_length=100, num_return_sequences=1)[0]["generated_text"]
    return f"Naya: {response.split('User query:')[1].strip()}"

# Test it
user_input = "What can you tell me about diabetes?"
print(get_naya_response(user_input))
