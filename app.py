import os
import streamlit as st
from core.chat_engine import get_llm_chain, conversation_flow
from core.history import (
    save_conversation,
    load_conversation,
    list_sorted_chats,
    generate_chat_id,
)

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

CONVERSATION_DIR = "saved_chats"
os.makedirs(CONVERSATION_DIR, exist_ok=True)

# Streamlit setup
st.set_page_config(page_title="Llama3 Chatbot 💬", layout="centered")
st.title("🤖 Chat with Llama3 7B 🦙")

# Load chat list
available_chats = list_sorted_chats()
chat_options = ["🆕 New chat"] + available_chats
selected_chat = st.sidebar.selectbox("📂 Select a chat", options=chat_options)

# New chat logic
if selected_chat == "🆕 New chat":
    if "new_chat_created" not in st.session_state:
        new_chat_id = generate_chat_id()
        st.session_state.message_history = [SystemMessage(content="You are a helpful assistant.")]
        st.session_state.current_chat = new_chat_id
        st.session_state.new_chat_created = True
        st.rerun()
    else:
        convo_id = st.session_state.current_chat
else:
    convo_id = selected_chat
    if "message_history" not in st.session_state or st.session_state.get("current_chat") != convo_id:
        st.session_state.message_history = load_conversation(convo_id)
        st.session_state.current_chat = convo_id
        if "new_chat_created" in st.session_state:
            del st.session_state.new_chat_created

# Use correct chat state
convo_id = st.session_state.get("current_chat", None)
message_history = st.session_state.get("message_history", [])

# Show previous messages
if convo_id:
    for msg in message_history:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.markdown(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(msg.content)

# LLM chain setup (done once)
if "llm_chain" not in st.session_state:
    st.session_state.llm_chain = get_llm_chain()

# Chat input
user_input = st.chat_input("Say something...")
if user_input and convo_id:
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.spinner("Reasoning..."):
        response = conversation_flow(st.session_state.llm_chain, message_history, user_input)
    with st.chat_message("assistant"):
        st.markdown(response)
    save_conversation(convo_id, message_history)
