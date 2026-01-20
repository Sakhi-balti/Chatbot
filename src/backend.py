from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()
HF_KEY = os.getenv('HF_KEY')
os.environ['LANGCHAIN_PROJECT']='Personal_Chatbot'

# Initialize LLM
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V3-0324",
    api_key=HF_KEY,
    base_url="https://router.huggingface.co/v1",
    temperature=0.7,
    max_tokens=500
)

# Define the state 
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Define chatbot node
def chatbot(state: State):
    """Main chatbot logic - processes messages and generates response"""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Build the graph
graph_builder = StateGraph(State)

# Add the chatbot node
graph_builder.add_node("chatbot", chatbot)

# Define the flow: START -> chatbot -> END
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Create the database
connection = sqlite3.connect(database = 'chatbot.db', check_same_thread = False)# we want to use for multiple thread check_same_thread =False
# Add memory to persist conversation
checkpointer = SqliteSaver(conn= connection)
graph = graph_builder.compile(checkpointer = checkpointer)

def retrieve_all_threads():
    try:
        all_thread = set()
        for checkpoint in checkpointer.list(None):
            if 'configurable' in checkpoint.config and 'thread_id' in checkpoint.config['configurable']:
                all_thread.add(checkpoint.config['configurable']['thread_id'])
        return list(all_thread)
    except:
        return []  