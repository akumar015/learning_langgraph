import streamlit as st
from backend import bot
from langchain_core.messages import HumanMessage


CONFIG={'configurable':{'thread_id': 'thread-1'}}


if 'history' not in st.session_state:
    st.session_state['history']=[]


for message in st.session_state['history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

#chat message (displays user/bot's message)

user_input=st.chat_input('Type here...')

if user_input:

    st.session_state['history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    response=bot.invoke({'message':[HumanMessage(content=user_input)]}, config=CONFIG)

    ai_message=response['message'][-1].text
    st.session_state['history'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)