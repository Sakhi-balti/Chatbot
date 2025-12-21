from logging import config
import streamlit as st
from backend import graph 
# Get user input
user_input = st.chat_input('Ask anything...')

if user_input:
    # Add user message to history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.write(user_input)

    # Add AI response to history (currently just echoing the input)
    CONFIG = {'configurable':{'thread_id':'1001'}}
    response = graph.invoke({"messages": [HumanMessage(content =  user_input)]}, config = CONFIG)
    ai_message = response['messages'][-1].content
       

    st.session_state['message_history'].append({'role': 'assistant', 'content':  ai_message})

    with st.chat_message('assistant'):
        st.write(ai_message)