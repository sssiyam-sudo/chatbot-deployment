import datetime
import os

CONVERSATION_DIR = "saved_chats"
os.makedirs(CONVERSATION_DIR, exist_ok=True)

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
