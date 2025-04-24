import os
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from langchain_core.messages import SystemMessage
from core.chat_engine import get_llm_chain, llmGen_withHistory
from core.history import load_conversation, save_conversation
from core.utils import generate_chat_id

app = FastAPI()
chain = get_llm_chain()

class ChatRequest(BaseModel):
    message: str
    chat_id: str | None = None

@app.post("/chat")
async def chat(payload: ChatRequest):
    chat_id = payload.chat_id or generate_chat_id()
    history = load_conversation(chat_id)

    if len(history) == 0:
        history.append(SystemMessage(content="You are a helpful assistant."))

    response = llmGen_withHistory(chain, history, payload.message)
    save_conversation(chat_id, history)

    return {
        "response": response,
        "chat_id": chat_id,
        "history": [m.content for m in history],
    }

@app.delete("/chat/{chat_id}")
async def delete_chat(chat_id: str):
    file_path = os.path.join("saved_chats", f"{chat_id}.json")

    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": f"Chat {chat_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Chat {chat_id} not found.")
    

