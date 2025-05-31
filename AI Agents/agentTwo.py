from typing import TypedDict, List, Union
from langchain_ollama import OllamaLLM
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]
    
def process_node(state: AgentState) -> AgentState:
    """
    This Nodes makes conversational with the LLMS
    """
    try:
        llm = OllamaLLM(model="llama3")
        response = llm.invoke(state["messages"])
        print(response)
        state["messages"].append(AIMessage(content=response))
        return state
    except Exception as e:
        print(e)
        return

graph = StateGraph(AgentState)

graph.add_node("process", process_node)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

convo_history = []

user_inp = input("Enter the Message: ")

while(user_inp != "exit"):
    convo_history.append(HumanMessage(content=user_inp))
    result = agent.invoke({"messages": convo_history})
    convo_history = result["messages"]
    user_inp = input("Enter: ")

with open("chat_history.txt", "w") as file:
    print("Writing data to the file\n")
    for message in convo_history:
        if(isinstance(message, HumanMessage)):
            file.write(f"You: {message.content}\n")
        if(isinstance(message, AIMessage)):
            file.write(f"AI: {message.content}\n")
    file.write("End of Conversation")
    
