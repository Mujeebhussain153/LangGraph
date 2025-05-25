from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str
    operation: str

def processor_node(state: AgentState) -> AgentState:
    """
    A function that processes the list of integers and performs operation based on the operation provided
    """
    try:
        if state['operation'] == "+":
            state['result'] = f"{state['name']}, the operation you performed is addition and the sum of all values is {sum(state['values'])}"
        elif state['operation'] == "*":
            pro = 1
            for i in state['values']:
                pro*=i
            state['result'] = f"{state['name']}, the operation you performed is multiplication and the product of all values is {pro}"
        return state
    except Exception as e:
        print(e)
        return

graph = StateGraph(AgentState)

graph.add_node('processor', processor_node)

graph.set_entry_point('processor')

graph.set_finish_point('processor')

app = graph.compile()

result = app.invoke({"name": "Mujeeb", "operation": "*", "values":[1,2,3,4,5]})

print(result['result'])
    