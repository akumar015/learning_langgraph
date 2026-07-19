from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages 
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
import operator

load_dotenv()

llm=ChatGoogleGenerativeAI(
    model='gemini-3.1-flash-lite'
)

class chatstate(TypedDict):
    message: Annotated[list[BaseMessage], add_messages]

def chatnode(state: chatstate):
    # take user query from state
    messages=state['message']

    #send to llm
    response=llm.invoke(messages)

    # return response to state
    return {'message': [response]}

checkpointer=MemorySaver()
graph=StateGraph(chatstate)

#nodes
graph.add_node('chatnode',chatnode)

#edges
graph.add_edge(START,'chatnode')
graph.add_edge('chatnode',END)

#compile
bot=graph.compile(checkpointer=checkpointer)

