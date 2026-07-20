import streamlit as st
from backend import bot
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig


CONFIG: RunnableConfig = {'configurable': {'thread_id': 'thread-1'}}


if 'history' not in st.session_state:
    st.session_state['history']=[]

# loading conversation history
for message in st.session_state['history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input=st.chat_input('Type here...')

if user_input:

    # add user's message to history
    st.session_state['history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    with st.chat_message('assistant'):
        ai_message=st.write_stream(
            message_chunk.text for message_chunk, metadata in bot.stream( #type:ignore
                {'message': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )
    st.session_state['history'].append({'role':'assistant','content': ai_message})