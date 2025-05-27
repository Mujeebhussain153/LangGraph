from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image

# Setting the Initial Schema of the State
class AgentState(TypedDict):
    num1: int
    num2: int
    operation: str
    num3: int
    num4: int
    operation2: str
    finaldata: int
    finaldata2: int


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
    
def adder2(state: AgentState) -> AgentState:
    """This Node adds the value of num3 and num4provided"""
    try:
        state['finaldata2'] = state['num3'] + state['num4']
        return state
    except Exception as e:
        print(e)
        return
    
def subtractor2(state: AgentState) -> AgentState:
    """This Node Subtracts the num3 and num4 provided"""
    try:
        state['finaldata2'] = state['num3'] - state['num4']
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
    
def decide_next2(state: AgentState) -> AgentState:
    """This Node decides the next node after execution of the first conditional graph"""
    try:
        if state['operation2'] == '+':
            return "add_operation2"
        
        elif state['operation2'] == '-':
            return "sub_operation2"
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

graph.add_node("router2", lambda state:state) # It does nothing, Just a State Passthrough function
graph.add_edge("adder", "router2")
graph.add_edge("subtractor", "router2")

graph.add_node("adder2", adder2)
graph.add_node("subtractor2", subtractor2)

graph.add_conditional_edges(
    "router2",
    decide_next2,
    {
        "add_operation2": "adder2",
        "sub_operation2": "subtractor2",
    }
)

graph.add_edge("adder2", END)
graph.add_edge("subtractor2", END)


app = graph.compile()
print(Image(app.get_graph().draw_png('hello.png')))

result = app.invoke(AgentState(num1=10, num2=2, operation="-", num3=7, num4=2, operation2='+'))

print(result['finaldata'], result['finaldata2'])