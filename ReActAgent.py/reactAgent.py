from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import SystemMessage, ToolMessage, BaseMessage
from langchain.agents import initialize_agent, AgentType
from langchain_ollama import OllamaLLM
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
@tool
def add(a: int, b: int) -> int:
    """This Tool adds a ,b and returns the result"""
    try:
        return a+b
    except Exception as e:
        print(e)
        return
@tool
def subtract(a: int, b: int) -> int:
    """This Tool subtracts a ,b and returns the result"""
    try:
        return a-b
    except Exception as e:
        print(e)
        return
@tool
def multiply(a: int, b: int) -> int:
    """This Tool multiplies a ,b and returns the result"""
    try:
        return a*b
    except Exception as e:
        print(e)
        return

tools = [add, subtract, multiply]

model = OllamaLLM(model="llama3").bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    try:
        response = model.invoke(state["messages"])
        return {"messages": [response]}
    except Exception as e:
        print(e)
        return
    
def should_continue(state: AgentState):
    try:
        messages = state["messages"]
        last_message = messages[-1]
        if not last_message.tool_calls:
            return "end"
        else:
            return "continue"
    except Exception as e:
        print(e)
        return

graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)


graph.add_edge(START, "our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)

graph.add_edge("tools", "our_agent")

app = graph.compile()

def print_stream(stream):
    for i in stream:
        message = i["messages"][-1]
        if(isinstance(message, tuple)):
            print(message)
        else:
            message.pretty_print()
        
inputs = {"messages": ["add 3 + 4. add 7 + 25. subtract 25-9. Multiply 7*7"]}

print_stream(app.stream(inputs, stream_mode="values"))
