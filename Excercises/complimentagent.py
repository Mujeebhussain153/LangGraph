# Importing Necessary Libraries
from typing import TypedDict
from langgraph.graph import StateGraph

# Initializing the ComplimentState TypedDict
class ComplimentState(TypedDict):
    name: str
    
def compliment_node(state: ComplimentState) -> ComplimentState:
    """
    A function that modifies the state by adding a name to the compliment message.
    """
    state['name'] = state['name'] +"You are doing great Job, Learning LangGraph!"
    return state

app = StateGraph(ComplimentState) \
    .add_node("complimenter", compliment_node) \
    .set_entry_point("complimenter") \
    .set_finish_point("complimenter") \
    .compile()
    
# Invoking the application with an initial state
result = app.invoke({"name": "Mujeeb, "})

print(result)