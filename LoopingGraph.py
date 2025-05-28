import random
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List

class AgentState(TypedDict):
    name: str
    values : List[int]
    counter: int
  
def greeting_node(state: AgentState) -> AgentState:
    """
    This Node just greets the user
    """
    state['name'] = f"Hey there {state['name']}"
    state['counter'] = 0
    return state

def random_node(state: AgentState) -> AgentState:
    """This Node just generates the random values"""
    random_data = random.randint(0, 10)
    state['values'].append(random_data)
    state['counter']+=1
    return state

def should_continue(state: AgentState) -> AgentState:
    """This node decides whether to continue to the next node or not"""
    if state['counter'] < 5:
        return "loop"
    else:
        return "exit"
    
graph = StateGraph(AgentState)

graph.add_node("greeter", greeting_node)
graph.add_node("random", random_node)
graph.add_edge("greeter", "random")

graph.add_conditional_edges(
    "random",
    should_continue,
    {
        "loop": "random",
        "exit": END
    }
)

graph.set_entry_point("greeter")
app = graph.compile()

result = app.invoke(AgentState(name="Mujeeb", values=[], counter=0))

print(result)