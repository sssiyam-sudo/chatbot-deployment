from operator import itemgetter
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, trim_messages

def get_llm_chain():
    llm = Ollama(model="llama3", base_url="http://192.168.1.3:11434")

    trimmer = trim_messages(
        max_tokens=1024,
        strategy="last",
        token_counter=llm,
        include_system=True,
        allow_partial=True,
        start_on="human"
    )

    system_prompt = "You are a helpful assistant. Your job is answering the user's questions very shortly."
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), MessagesPlaceholder(variable_name="messages")])

    return RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer) | prompt | llm

def conversation_flow(chain, message_history, user_input):
    llm_generation = chain.invoke({"messages": message_history + [HumanMessage(content=user_input)]})
    message_history.append(HumanMessage(content=user_input))
    message_history.append(AIMessage(content=llm_generation))
    return llm_generation
