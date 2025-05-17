import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content="You are a helpful assistant with a friendly, witty tone, inspired by Grok from xAI. Keep responses concise and engaging!")]
if "messages" not in st.session_state:
    st.session_state.messages = []

# Custom CSS for Grok-like UI (dark theme, chat bubbles, modern look)
st.markdown("""
    <style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
        font-family: 'Arial', sans-serif;
    }
    .chat-container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
    }
    .user-message {
        background-color: #3A3A3A;
        color: #FFFFFF;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        max-width: 70%;
        align-self: flex-end;
        text-align: right;
    }
    .ai-message {
        background-color: #6200EA;
        color: #FFFFFF;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        max-width: 70%;
        align-self: flex-start;
    }
    .chat-input {
        position: fixed;
        bottom: 20px;
        width: 100%;
        max-width: 800px;
        padding: 10px;
        background-color: #2A2A2A;
        border-radius: 10px;
    }
    .stTextInput > div > input {
        background-color: #3A3A3A;
        color: #FFFFFF;
        border-radius: 10px;
        border: none;
        padding: 10px;
    }
    .stButton > button {
        background-color: #6200EA;
        color: #FFFFFF;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
    }
    .stButton > button:hover {
        background-color: #7F39FB;
    }
    .sidebar .stTextInput > div > input {
        background-color: #3A3A3A;
        color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for API key and settings
with st.sidebar:
    st.header("⚙️ Settings")
    google_api_key = st.text_input("Google API Key", type="password", help="Enter your Google API key for Gemini.")
    if google_api_key:
        os.environ["GOOGLE_API_KEY"] = google_api_key
    st.markdown("---")
    st.markdown("Built with ❤️ by an xAI fan! Powered by Streamlit & Gemini.")

# Initialize LLM
try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")  # Using gemini-1.5-flash (replace with gemini-2.0-flash if available)
except Exception as e:
    st.error("Failed to initialize LLM. Please check your API key or model availability.")
    st.stop()

# Main app layout
st.title("🤖 Grok Bhaiya")
st.markdown("Your friendly AI assistant, inspired by xAI's Grok. Chat with me! 😎", unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">You: {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-message">Grok Bhaiya: {message["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
st.markdown('<div class="chat-input">', unsafe_allow_html=True)
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message...", key="user_input")
    submit_button = st.form_submit_button("Send")
st.markdown('</div>', unsafe_allow_html=True)

# Handle user input
if submit_button and user_input:
    if user_input.lower() == "quit":
        st.session_state.chat_history = [SystemMessage(content="You are a helpful assistant with a friendly, witty tone, inspired by Grok from xAI. Keep responses concise and engaging!")]
        st.session_state.messages = []
        st.experimental_rerun()

    # Add user message to history
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response
    try:
        with st.spinner("Grok Bhaiya is thinking..."):
            result = llm.invoke(st.session_state.chat_history)
            ai_response = result.content
            st.session_state.chat_history.append(AIMessage(content=ai_response))
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Oops! Something went wrong: {str(e)}")

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.chat_history = [SystemMessage(content="You are a helpful assistant with a friendly, witty tone, inspired by Grok from xAI. Keep responses concise and engaging!")]
    st.session_state.messages = []
    st.experimental_rerun()
