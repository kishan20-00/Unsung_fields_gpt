import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "deepseek-r1-distill-llama-70b"  # Default model

# Sidebar
st.sidebar.title("Unsung Fields Cloud")
st.sidebar.button("Documentation")
st.sidebar.button("Metrics")
st.sidebar.button("API Keys")
st.sidebar.button("Settings")
st.sidebar.markdown("---")
st.sidebar.button("Status")
st.sidebar.button("Discord")
st.sidebar.button("Chat with us")

# Main interface
st.title("Playground")

# Top-right model selection
selected_model = st.selectbox(
    "Select Model",
    options=[
        "deepseek-r1-distill-llama-70b",
        "distil-whisper-large-v3-en",
        "gemma2-9b-it",
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama-guard-3-8b",
        "llama3-70b-8192",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "whisper-large-v3",
        "whisper-large-v3-turbo",
    ],
    key="model_selector",
    index=[
        "deepseek-r1-distill-llama-70b",
        "distil-whisper-large-v3-en",
        "gemma2-9b-it",
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama-guard-3-8b",
        "llama3-70b-8192",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "whisper-large-v3",
        "whisper-large-v3-turbo",
    ].index(st.session_state.selected_model),
)

# Store the selected model in session state
st.session_state.selected_model = selected_model

# Parameters Section
st.subheader("Parameters")
temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.5, step=0.1)
max_tokens = st.slider("Max Completion Tokens", min_value=1, max_value=8092, value=1024, step=1)
stream = st.checkbox("Stream", value=False)
json_mode = st.checkbox("JSON Mode", value=False)

# Advanced Section (Collapsible)
with st.expander("Advanced"):
    llamaguard = st.checkbox("Llamaguard", value=False)
    if llamaguard:
        st.session_state.selected_model = "llama-guard-3-8b"  # Set model to llama-guard-3-8b when checkbox is clicked
    top_p = st.slider("Top-P", min_value=0.0, max_value=1.0, value=1.0, step=0.01)
    seed = st.number_input("Seed", min_value=0, step=1, value=0, help="Random seed for reproducibility.")
    stop_sequence = st.text_input("Stop Sequence", placeholder="Enter stop sequence")

# Chat Interface
st.subheader("Chat")
user_message = st.text_input("Enter your message:", key="user_input", placeholder="Type here...")

if st.button("Send"):
    if user_message:
        # Append the user's message to chat history
        st.session_state.chat_history.append(("user", user_message))

        # Call Groq API for response
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message},
                ],
                model=selected_model,
                temperature=temperature,
                max_completion_tokens=max_tokens,
                top_p=top_p,
                stop=stop_sequence or None,
                stream=stream,
            )

            if stream:
                # Handle streaming response
                system_message = ""
                for chunk in chat_completion:
                        delta_content = chunk.choices[0].delta.content
                        if delta_content:  # Check if delta_content is not None
                                system_message += delta_content

            else:
                # Handle non-streaming response
                system_message = chat_completion.choices[0].message.content

        except Exception as e:
            system_message = f"Error: {e}"

        # Append the system's message to chat history
        st.session_state.chat_history.append(("system", system_message))

# Display Chat History
for role, message in st.session_state.chat_history:
    if role == "user":
        st.markdown(
            f"""
            <div style="text-align: right; margin-bottom: 10px;">
                <div style="display: inline-block; background-color: #DCF8C6; color: black; padding: 10px; border-radius: 10px;">
                    {message}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif role == "system":
        st.markdown(
            f"""
            <div style="text-align: left; margin-bottom: 10px;">
                <div style="display: inline-block; background-color: #E6E6E6; color: black; padding: 10px; border-radius: 10px;">
                    {message}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    """
    ---
    **Welcome to the Playground**
    - You can start chatting by typing a message.
    - Your message appears on the right, and the system's response on the left.
    """
)
