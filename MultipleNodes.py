from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    values : List[int]
    result : str
    
def first_node(state: AgentState) -> AgentState:
    """
    This Function just takes the name and concatenates to a string
    """
    try:
        state['result'] = f"{state['name']}, your sum is calculated and it is"
        return state
    except Exception as e:
        print(e)
        return
    
def second_node(state: AgentState) -> AgentState:
    """
    This Function just takes state of the previous node, calculates the sum and then returns the updated state
    """
    try:
        s = sum(state['values'])
        state['result'] = state['result'] + f" {s}"
        return state
    except Exception as e:
        print(e)
        return

graph = StateGraph(AgentState)

graph.add_node("first_node", first_node)

graph.add_node("second_node", second_node)

graph.add_edge("first_node", "second_node")

graph.set_entry_point("first_node")
graph.set_finish_point("second_node")

# Graph Will look something like this

    #    Start
    #      |
    #  first_node
    #      |
    #  second_node
    #      |
    #     Stop
    
app = graph.compile()

result = app.invoke({"name": "Mujeeb", "values":[1,2,3,4,5]})

print(result['result'])