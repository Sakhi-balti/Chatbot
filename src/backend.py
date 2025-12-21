from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os

load_dotenv()
HF_KEY = os.getenv('HF_KEY')

# Initialize LLM
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V3-0324",
    api_key=HF_KEY,
    base_url="https://router.huggingface.co/v1",
    temperature=0.7,
    max_tokens=500
)

# Define the state structure
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Define the chatbot node
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

# Add memory to persist conversation
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

