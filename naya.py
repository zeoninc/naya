import streamlit as st
import requests
import json
from datetime import datetime

# Ollama API endpoint (local for now)
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Mock patient data (expandable to a database later)
MOCK_PATIENTS = {
    "MRN001": {
        "name": "John Doe",
        "history": "Hypertension, Diabetes",
        "labs": "BP: 120/80, Glucose: 120",
        "notes": "Stable, follow-up in 3 months"
    },
    "MRN002": {
        "name": "Jane Smith",
        "history": "Asthma",
        "labs": "BP: 110/70, Oxygen: 95%",
        "notes": "Recent wheezing episode"
    }
}

# Initialize session state for chat history and channels
if "channels" not in st.session_state:
    st.session_state.channels = {"General": []}  # General chat + patient-specific channels
if "current_channel" not in st.session_state:
    st.session_state.current_channel = "General"

# Function to get Naya's response from Ollama
def get_naya_response(prompt, mrn=None):
    base_prompt = "You are Naya, an AI healthcare assistant designed to provide helpful and accurate information with a friendly, professional tone."
    if mrn and mrn in MOCK_PATIENTS:
        patient = MOCK_PATIENTS[mrn]
        context = f"Patient MRN: {mrn}, Name: {patient['name']}, History: {patient['history']}, Labs: {patient['labs']}, Notes: {patient['notes']}."
        full_prompt = f"{base_prompt} {context} User query: {prompt}"
    else:
        full_prompt = f"{base_prompt} User query: {prompt}"

    payload = {
        "model": "naya",  # Assuming your Ollama model is tagged as "naya"
        "prompt": full_prompt,
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

# Sidebar for channel management
with st.sidebar:
    st.header("Naya Channels")
    
    # Menu options
    menu = st.selectbox("Menu", ["Chat", "Create Channel"])
    
    if menu == "Chat":
        # Display existing channels
        st.subheader("Active Channels")
        for channel in st.session_state.channels.keys():
            if st.button(channel, key=f"btn_{channel}"):
                st.session_state.current_channel = channel
    
    elif menu == "Create Channel":
        # Create new patient-specific channel
        st.subheader("Create a New Channel")
        mrn = st.text_input("Enter Patient MRN (e.g., MRN001):")
        if st.button("Create") and mrn:
            if mrn in MOCK_PATIENTS:
                if mrn not in st.session_state.channels:
                    st.session_state.channels[mrn] = []
                    st.success(f"Channel for {mrn} created!")
                else:
                    st.warning("Channel already exists!")
            else:
                st.error("MRN not found in patient database.")
        elif not mrn and st.button("Create"):
            st.warning("Please enter an MRN.")

# Main app layout
st.title("Naya - AI Healthcare Assistant")
st.write(f"Current Channel: **{st.session_state.current_channel}**")

# Display patient info if in a patient-specific channel
if st.session_state.current_channel != "General" and st.session_state.current_channel in MOCK_PATIENTS:
    patient = MOCK_PATIENTS[st.session_state.current_channel]
    with st.expander(f"Patient Info - {patient['name']} (MRN: {st.session_state.current_channel})", expanded=True):
        st.write(f"**History:** {patient['history']}")
        st.write(f"**Labs:** {patient['labs']}")
        st.write(f"**Notes:** {patient['notes']}")

# Chat interface
chat_container = st.container()
with chat_container:
    # Display chat history
    for message in st.session_state.channels[st.session_state.current_channel]:
        if message["role"] == "user":
            st.markdown(f"**You ({message['time']}):** {message['text']}")
        else:
            st.markdown(f"**Naya ({message['time']}):** {message['text']}")

# Input area at the bottom
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_area("Type your message:", height=100)
    submit_button = st.form_submit_button(label="Send")

# Process input and get response
if submit_button and user_input:
    # Add user message to current channel
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.channels[st.session_state.current_channel].append({
        "role": "user",
        "text": user_input,
        "time": timestamp
    })
    
    # Get Naya’s response
    with st.spinner("Naya is thinking..."):
        response = get_naya_response(user_input, mrn=st.session_state.current_channel if st.session_state.current_channel != "General" else None)
    
    # Add Naya’s response to current channel
    st.session_state.channels[st.session_state.current_channel].append({
        "role": "naya",
        "text": response,
        "time": datetime.now().strftime("%H:%M:%S")
    })
    
    # Refresh page to show updated chat
    st.rerun()

# Styling tweak for better chat flow
st.markdown("""
    <style>
    .stTextArea { margin-bottom: 10px; }
    .stButton { margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)