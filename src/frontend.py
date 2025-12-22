import streamlit as st
from backend import graph 
from langchain_core.messages import HumanMessage

# *********************************Session Setup***************************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []



# Display existing chat history
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
    CONFIG = {'configurable': {'thread_id': '1001'}}
    
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