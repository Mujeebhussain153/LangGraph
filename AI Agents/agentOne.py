from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langchain_ollama import OllamaLLM

class AgentState(TypedDict):
    message: List[HumanMessage]
    
llm = OllamaLLM(model="llama3")

def process_node(state: AgentState) -> AgentState:
    try:
        response = llm.invoke(state['message'])
        print(response)
        return state
    except Exception as e:
        print(e)
        return
    
graph = StateGraph(AgentState)

graph.add_node("process", process_node)

graph.add_edge(START, "process")

graph.add_edge('process', END)

agent = graph.compile()

user_input = input("Enter the Message: ")

while user_input != "exit":
    agent.invoke({"message": [HumanMessage(content=user_input)]})
    user_input = input("Enter: ")