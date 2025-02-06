import streamlit as st

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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
st.markdown(
    """
    <div style="display: flex; justify-content: flex-end; align-items: center; margin-bottom: 10px;">
        <label for="model-select" style="margin-left: 10px; font-size: 16px;">Select Model:</label>
    </div>
    """,
    unsafe_allow_html=True,
)
selected_model = st.selectbox("", options=["deepseek-r1-distill-llama-70b", "distil-whisper-large-v3-en", "gemma2-9b-it", "llama-3.3-70b-versatile", "llama-3.1-8b-instant", "llama-guard-3-8b", "llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "whisper-large-v3", "whisper-large-v3-turbo"], key="model_selector")

# Parameters Section
st.subheader("Parameters")
temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
max_tokens = st.slider("Max Completion Tokens", min_value=1, max_value=8092, value=1024, step=1)
stream = st.checkbox("Stream", value=True)
json_mode = st.checkbox("JSON Mode", value=False)

# Advanced Section (Collapsible)
with st.expander("Advanced"):
    llamaguard = st.checkbox("Llamaguard", value=False)
    top_p = st.slider("Top-P", min_value=0.0, max_value=1.0, value=0.9, step=0.01)
    seed = st.number_input("Seed", min_value=0, step=1, value=42, help="Random seed for reproducibility.")
    stop_sequence = st.text_input("Stop Sequence", placeholder="Enter stop sequence")


# Chat Interface
st.subheader("Chat")
user_message = st.text_input("Enter your message:", key="user_input", placeholder="Type here...")

if st.button("Send"):
    if user_message:
        # Append the user's message to chat history
        st.session_state.chat_history.append(("user", user_message))
        # Placeholder for system output (you can replace this with real output later)
        system_message = f"Echo: {user_message}"  # Replace this with system response logic
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