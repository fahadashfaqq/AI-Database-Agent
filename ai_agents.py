from typing import Annotated
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from Tools import tools



load_dotenv()



class AgentState(dict):
    messages: Annotated[list[BaseMessage], add_messages]



SYSTEM_PROMPT = """
You are an AI assistant for user management.

You help the administrator manage users through natural language commands.

You can perform the following operations:

1. Create a user
2. Search for a user
3. Update a user
4. Delete a user

Rules:

- Always use the available tools when working with the database.
- Never invent user information or user IDs.
- If you need to update or delete a user and the user ID is unknown,
  search for the user first.
- If multiple users have similar names, ask the administrator for clarification.
- Do not guess which user the administrator means.
- Do not say an operation was successful unless the tool confirms it.
- Respond clearly and briefly.

Response formatting rules:

- Respond clearly, briefly, and professionally.
- Do not display raw Python lists, dictionaries, JSON, SQL queries, or tool output.
- Do not include internal database IDs unless specifically requested.

- When displaying a single user, use exactly this format:

Name: [name]
Email: [email]
Phone: [phone]
City: [city]

- When displaying multiple users, each user MUST be displayed on separate lines.

Use exactly this format:

Here are the users:

1.
Name: Fahad
Email: fahad@gmail.com
Phone: 03084544004
City: Sialkot

2.
Name: Ali
Email: ali@gmail.com
Phone: 03123456789
City: Lahore

- NEVER put multiple user fields on the same line.
- ALWAYS use line breaks between Name, Email, Phone, and City.
- Do not write all user information in a single paragraph.

"""



llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)



llm_with_tools = llm.bind_tools(tools)


# Agent node
def agent(state):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


# Create LangGraph workflow
graph = StateGraph(AgentState)



graph.add_node(
    "agent",
    agent
)



graph.add_node(
    "tools",
    ToolNode(tools)
)


# Start with agent
graph.set_entry_point("agent")


# Decide whether to call tools or finish
graph.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        END: END
    }
)


# After a tool is called, return to agent
graph.add_edge(
    "tools",
    "agent"
)


# Compile the graph
agent_graph = graph.compile()



def run_agent(user_message: str):

    result = agent_graph.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }
    )

    final_message = result["messages"][-1]

    return final_message.content