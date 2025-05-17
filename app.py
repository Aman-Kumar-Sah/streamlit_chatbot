import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os
os.envirom["GOOGLE_APP_KEY"] = st.secrets["GOOGLE_APP_KEY"]

# Initialize the LLM (ensure your API key is set as an environment variable or in config)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

st.set_page_config(page_title="Gemini Chat", page_icon="🤖")

st.title("💬 Gemini Chatbot")
st.markdown("Talk to Gemini 2.0 Flash using LangChain and Streamlit!")

# Initialize session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content="You are a helpful assistant.")]

# Input from user
user_input = st.chat_input("Type your message...")

# When user submits input
if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Invoke model
    response = llm.invoke(st.session_state.chat_history)
    st.session_state.chat_history.append(AIMessage(content=response.content))

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(response.content)

# Show entire history in expandable panel (optional)
with st.expander("🧠 Chat History (Debug)", expanded=False):
    for msg in st.session_state.chat_history:
        role = type(msg).__name__.replace("Message", "")
        st.write(f"**{role}**: {msg.content}")

