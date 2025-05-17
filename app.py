import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os

# Set Google API key from Streamlit secrets
try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("Google API key not found in Streamlit secrets. Please configure it.")
    st.stop()

# Initialize the LLM (Gemini 2.0 Flash)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Configure Streamlit page
st.set_page_config(page_title="Gemini Chat", page_icon="🤖")
st.title("💬 Gemini Chatbot")
st.markdown("Interact with Gemini 2.0 Flash using LangChain and Streamlit!")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content="You are a helpful assistant.")]

# User input field
user_input = st.chat_input("Type your message...")

# Handle user input
if user_input:
    # Append user message to chat history
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    try:
        # Get AI response from the model
        response = llm.invoke(st.session_state.chat_history)
        st.session_state.chat_history.append(AIMessage(content=response.content))
        
        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(response.content)
    except Exception as e:
        st.error(f"Error getting response from model: {e}")

# Display chat history in an expandable debug panel
with st.expander("🧠 Chat History (Debug)", expanded=False):
    for msg in st.session_state.chat_history:
        role = msg.__class__.__name__.replace("Message", "")
        st.write(f"**{role}**: {msg.content}")

