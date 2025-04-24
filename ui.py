import streamlit as st
import requests
from core.history import load_conversation, save_conversation
from core.utils import list_sorted_chats, generate_chat_id 
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

#API_URL = "http://localhost:8000/chat"
API_URL = "http://172.20.247.252:8000/chat"


# Streamlit setup
st.set_page_config(page_title="Llama3 Chatbot 💬", layout="centered")
st.title("🤖 Chat with Llama3 7B 🦙")

available_chats = list_sorted_chats()
chat_options = ["🆕 New chat"] + available_chats
selected_chat = st.sidebar.selectbox("📂 Select a chat", options=chat_options)

if selected_chat == "🆕 New chat":
    if "new_chat_created" not in st.session_state:
        new_chat_id = generate_chat_id()
        st.session_state.message_history = [SystemMessage(content = "You are a helpful assistant.")]
        st.session_state.current_chat = new_chat_id
        st.session_state.new_chat_created = True
    else:
        convo_id = st.session_state.current_chat
else:
    convo_id = selected_chat
    if "message_history" not in st.session_state or st.session_state.get("current_chat") != convo_id:
        st.session_state.message_history = load_conversation(convo_id)
        st.session_state.current_chat = convo_id
        if "new_chat_created" in st.session_state:
            del st.session_state.new_chat_created

# Show deleting option for existing chats
if selected_chat != "🆕 New chat":
    if st.sidebar.button("🗑️ Delete selected chat"):
        delete_url = f"{API_URL}/{selected_chat}"
        delete_response = requests.delete(delete_url)

        if delete_response.status_code == 200:
            st.session_state.chat_deleted = True  # ✅ set a flag
            if "current_chat" in st.session_state:
                del st.session_state["current_chat"]
            if "message_history" in st.session_state:
                del st.session_state["message_history"]
            st.rerun()
        else:
            st.sidebar.error("❌ Failed to delete chat.")
if st.session_state.get("chat_deleted"):
    st.sidebar.success("✅ Chat deleted successfully.")
    del st.session_state["chat_deleted"]



# Get current chat state
convo_id = st.session_state.get("current_chat", None)
message_history = st.session_state.get("message_history", [])

# Display chat history
if convo_id:
    for msg in message_history:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.markdown(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(msg.content)

# Send message to FastAPI and update chat
def send_to_api(message, chat_id):
    response = requests.post(API_URL, json={"message": message, "chat_id":chat_id})
    if response.status_code == 200:
        data = response.json ()
        return data["response"]
    else:
        return "⚠️ Failed to connect to the backend API."
    

# Handle input
user_input = st.chat_input("Say something...")
if user_input and convo_id:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        api_response = send_to_api(user_input, convo_id)

    with st.chat_message("assistant"):
        st.markdown(api_response)

    # Locally update session state and save
    st.session_state.message_history.append(HumanMessage(content=user_input))
    st.session_state.message_history.append(AIMessage(content=api_response))
    save_conversation(convo_id, st.session_state.message_history)


