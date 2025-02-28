import streamlit as st
from transformers import pipeline

# Load model (distilgpt2 for now, replace with Llama-2-7b-hf later)
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="distilgpt2")

generator = load_model()

def get_naya_response(user_input):
    prompt = f"You are Naya, an AI healthcare assistant designed to provide helpful and accurate information with a friendly, professional tone. User query: {user_input}"
    response = generator(prompt, max_length=100, num_return_sequences=1)[0]["generated_text"]
    return f"Naya: {response.split('User query:')[1].strip()}"

# Streamlit interface
st.title("Naya - Your AI Healthcare Assistant")
st.write("Ask Naya anything about health or medicine!")

user_input = st.text_input("Your question:")
if st.button("Ask Naya"):
    if user_input:
        with st.spinner("Naya is thinking..."):
            response = get_naya_response(user_input)
        st.text_area("Naya’s Response:", value=response, height=200)
    else:
        st.warning("Please enter a question!")
