from typing import TypedDict, Sequence, Annotated
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, ToolMessage, SystemMessage
from langgraph.graph.message import add_messages
from langchain_experimental.llms import ollama_functions
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langchain.tools import tool

# This is a global document that can be utilized by the agent to update or save
document_content = ""

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
@tool
def update_doc(content: str) -> str:
    "Updates the document with provided content"
    try:
        global document_content
        document_content = content
        return f"Document has been updated successfully! The current content is:\n{document_content}"
    except Exception as e:
        print(e)
        return
    
@tool
def save_doc(filename) -> str:
    """Save the current document to a text file and finish the process.
    
    Args:
        filename: Name for the text file.
    """
    try:
        global document_content
        if(not filename):
            filename = filename+".txt"
        with open(filename, 'w') as file:
            file.write(document_content)
        print(f"\n💾 Document has been saved to: {filename}")
        return f"Document has been saved successfully to '{filename}'."
    except Exception as e:
        return f"Error saving document: {str(e)}"

tools = [update_doc, save_doc]

#initialized the model that i'm about to use
model = ollama_functions.OllamaFunctions(model="llama3").bind_tools(tools)

def our_agent(state: AgentState) -> AgentState:
    try:
        system_prompt = SystemMessage(content=f"""
        You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.
        
        - If the user wants to update or modify content, use the 'update_doc' tool with the complete updated content.
        - If the user wants to save and finish, you need to use the 'save_doc' tool.
        - Make sure to always show the current document state after modifications.
        
        The current document content is:{document_content}
        """)

        # if not state["messages"]:
        #     user_input = "I'm ready to help you update a document. What would you like to create?"
        #     user_message = HumanMessage(content=user_input)

        # else:
        user_input = input("\nWhat would you like to do with the document? ")
        print(f"\n👤 USER: {user_input}")
        user_message = HumanMessage(content=user_input)

        all_messages = [system_prompt] + list(state["messages"]) + [user_message]

        response = model.invoke(all_messages)

        print(f"\n🤖 AI: {response}")
        if hasattr(response, "tool_calls") and response.tool_calls:
            print(f"🔧 USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")

        return {"messages": list(state["messages"]) + [user_message, response]}
    except Exception as e:
        print(e)
        return
    
def should_continue(state: AgentState) -> str:
    """Determine if we should continue or end the conversation."""

    messages = state["messages"]
    
    if not messages:
        return "continue"
    
    # This looks for the most recent tool message....
    for message in reversed(messages):
        # ... and checks if this is a ToolMessage resulting from save
        if (isinstance(message, ToolMessage) and 
            "saved" in message.content.lower() and
            "document" in message.content.lower()):
            return "end" # goes to the end edge which leads to the endpoint
        
    return "continue"

def print_messages(messages):
    """Function I made to print the messages in a more readable format"""
    if not messages:
        return
    
    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"\n🛠️ TOOL RESULT: {message.content}")


graph = StateGraph(AgentState)

graph.add_node("agent", our_agent)
graph.add_node("tools", ToolNode(tools))

graph.set_entry_point("agent")

graph.add_edge("agent", "tools")


graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        "continue": "agent",
        "end": END,
    },
)

app = graph.compile()

def run_document_agent():
    print("\n ===== DRAFTER =====")
    
    state = {"messages": [AIMessage(content="I'm ready to help you update a document. What would you like to create?")]}
    
    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])
    
    print("\n ===== DRAFTER FINISHED =====")

if __name__ == "__main__":
    run_document_agent()


