import os
import json
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

CONVERSATION_DIR = "saved_chats"
os.makedirs(CONVERSATION_DIR, exist_ok=True)

def load_conversation(convo_id):
    filepath = os.path.join(CONVERSATION_DIR, f"{convo_id}.json")
    if not os.path.exists(filepath):
        return [SystemMessage(content="You are a helpful assistant.")]
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    msg_type_map = {"HumanMessage": HumanMessage, "AIMessage": AIMessage, "SystemMessage": SystemMessage}
    return [msg_type_map[item["type"]](content=item["content"]) for item in data]


def save_conversation(convo_id, messages):
    data = [{"type": type(m).__name__, "content": m.content} for m in messages]
    with open(os.path.join(CONVERSATION_DIR, f"{convo_id}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)