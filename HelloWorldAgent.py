# Import necessary libraries
from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    message: str
    
def greeting_node(state: AgentState) -> AgentState:
    """
    A simple function that modifies the state by adding a greeting message.
    """
    state['message'] = "Hello "+ state['message'] + " ,How is Your Day Going?"
    return state

# Create a state graph
# This graph will have a single node that modifies the state
graph = StateGraph(AgentState)

# Add a node to the graph
graph.add_node("greeter", greeting_node)
# Set the entry and finish points of the graph
graph.set_entry_point("greeter")

graph.set_finish_point("greeter")

# Compile the graph into an application
# This step prepares the graph for execution
app = graph.compile()

# Invoke the application with an initial state
result = app.invoke(
    AgentState(message="Mujeeb")
)

print(result)