import os
import json
import datetime
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

CONVERSATION_DIR = "saved_chats"
os.makedirs(CONVERSATION_DIR, exist_ok=True)

def save_conversation(convo_id, messages):
    data = [{"type": type(m).__name__, "content": m.content} for m in messages]
    with open(os.path.join(CONVERSATION_DIR, f"{convo_id}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_conversation(convo_id):
    filepath = os.path.join(CONVERSATION_DIR, f"{convo_id}.json")
    if not os.path.exists(filepath):
        return [SystemMessage(content="You are a helpful assistant.")]
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    msg_type_map = {"HumanMessage": HumanMessage, "AIMessage": AIMessage, "SystemMessage": SystemMessage}
    return [msg_type_map[item["type"]](content=item["content"]) for item in data]

def extract_timestamp(name):
    try:
        return datetime.datetime.strptime(name.replace("Chat_", ""), "%Y-%m-%d_%H-%M-%S")
    except:
        return datetime.datetime.min

def list_sorted_chats():
    chats = [
        f.replace(".json", "")
        for f in os.listdir(CONVERSATION_DIR)
        if f.endswith(".json")
    ]
    chats.sort(key=extract_timestamp, reverse=True)
    return chats

def generate_chat_id():
    now = datetime.datetime.now()
    return now.strftime("Chat_%Y-%m-%d_%H-%M-%S")
