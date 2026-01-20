
# ---------------------------------------------------------Implement SQlite------------------------------
import streamlit as st
from backend import graph, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid 
from datetime import datetime
# ********************************* utility functions ***********************************
def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id  not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    try:
        messages = graph.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']
        temp_messages = []
        for message in messages:
            role = 'user' if isinstance(message, HumanMessage) else 'assistant'
            temp_messages.append({'role': role, 'content': message.content})
        return temp_messages
    except Exception as e:
        st.error(f"Error loading conversation: {str(e)}")
        return []

# ********************************* Session Setup******************************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])


# *********************************** Sidebar Section *******************************************
st.sidebar.title('🤖 S.H_Chatbot')

if st.sidebar.button('➕ New Chat', use_container_width=True):
    reset_chat()

st.sidebar.divider()
st.sidebar.header('Recent Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        st.session_state['message_history'] = load_conversation(thread_id)

#******************************************* Main UI *****************************************
st.title('Chat Assistant')

# Display current thread ID in small text
st.caption(f"Thread: {st.session_state['thread_id'][:8]}...")

# Display message history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.write(message['content'])

# Get user input
user_query = st.chat_input('Ask anything...')

if user_query:
    # Add user message to history
    st.session_state['message_history'].append({'role': 'user', 'content': user_query})
    
    # Display user message
    with st.chat_message('user'):
        st.write(user_query)

    # Configuration for LangGraph
    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']},
              'metadata':{
                  'thread_id':st.session_state['thread_id']
              },
              'run_name':'chat_turn'}
    
    # Display AI response with streaming
    with st.chat_message('assistant'):
        # Create a generator function for streaming
        def generate_response():
            for message_chunk, metadata in graph.stream(
                {'messages': [HumanMessage(content=user_query)]},
                config=CONFIG,
                stream_mode='messages'
            ):
                if message_chunk.content:
                    yield message_chunk.content
        
        # Stream and capture the response
        ai_message = st.write_stream(generate_response())
    
    # Add AI response to history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})