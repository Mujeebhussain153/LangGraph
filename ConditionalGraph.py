from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# Setting the Initial Schema of the State
class AgentState(TypedDict):
    num1: int
    num2: int
    operation: str
    finaldata: int


def adder(state: AgentState) -> AgentState:
    """This Node adds the value of two numbers provided"""
    try:
        state['finaldata'] = state['num1'] + state['num2']
        return state
    except Exception as e:
        print(e)
        return
    
def subtractor(state: AgentState) -> AgentState:
    """This Node Subtracts the value of two numbers provided"""
    try:
        state['finaldata'] = state['num1'] - state['num2']
        return state
    except Exception as e:
        print(e)
        return

def decide_next(state: AgentState) -> AgentState:
    """This Node decides the next node of the graph"""
    try:
        if state['operation'] == '+':
            return "add_operation"
        
        elif state['operation'] == '-':
            return "sub_operation"
    except Exception as e:
        print(e)
        return
    

graph = StateGraph(AgentState)

graph.add_node("adder", adder)
graph.add_node("subtractor", subtractor)
graph.add_node("router", lambda state:state) # It does nothing, Just a State Passthrough function

graph.add_edge(START, "router")

graph.add_conditional_edges(
    "router",
    decide_next,
    {
        "add_operation": "adder",
        "sub_operation": "subtractor",
    }
)

graph.add_edge("adder", END)
graph.add_edge("subtractor", END)

app = graph.compile()

result = app.invoke(AgentState(num1=5, num2=3, operation="-"))
result = app.invoke(AgentState(num1=5, num2=3, operation="+"))

print(result['finaldata'])