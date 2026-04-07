"""
Recipe Agent — Custom LangGraph Agent
Fetches recipes from TheMealDB API using tool-calling nodes.
"""

from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from config.settings import get_llm
from tools.recipe_tools import (
    search_recipe_by_name,
    get_random_recipe,
    search_recipes_by_category,
)


# ── State ──────────────────────────────────────────────────────────────────────

class RecipeState(TypedDict):
    messages: Annotated[list, add_messages]


# ── Tools ──────────────────────────────────────────────────────────────────────

RECIPE_TOOLS = [search_recipe_by_name, get_random_recipe, search_recipes_by_category]
TOOLS_BY_NAME = {t.name: t for t in RECIPE_TOOLS}


# ── Helper ─────────────────────────────────────────────────────────────────────

def _normalize_content(content) -> str:
    """Convert Gemini/LangChain content into clean plain text."""
    if not content:
        return ""

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text" and item.get("text"):
                    parts.append(item["text"])
                elif item.get("text"):
                    parts.append(str(item["text"]))
            elif isinstance(item, str):
                parts.append(item)
            else:
                parts.append(str(item))
        return "\n".join(part for part in parts if part).strip()

    if isinstance(content, dict):
        if content.get("text"):
            return str(content["text"]).strip()
        return str(content).strip()

    return str(content).strip()


# ── Nodes ──────────────────────────────────────────────────────────────────────

def recipe_model_node(state: RecipeState, config: RunnableConfig):
    """LLM node — decides which tool to call or formats final answer."""
    llm = get_llm(temperature=0.3)
    llm_with_tools = llm.bind_tools(RECIPE_TOOLS)

    system_prompt = (
        "You are ChefMate AI's Recipe Agent. "
        "Your job is to help users find recipes using real tool data. "
        "Use search_recipe_by_name for specific recipe queries, "
        "get_random_recipe for surprise meals, and "
        "search_recipes_by_category for category browsing. "
        "Always call the appropriate tool first when recipe data is needed. "
        "After receiving tool results, respond with a clean, user-friendly recipe answer. "
        "Do not expose raw tool output, JSON, Python objects, or internal formatting."
    )

    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm_with_tools.invoke(messages, config)
    return {"messages": [response]}


def recipe_tool_node(state: RecipeState):
    """Tool execution node — runs the selected tool."""
    last_message = state["messages"][-1]
    tool_results = []

    for tool_call in last_message.tool_calls:
        tool = TOOLS_BY_NAME.get(tool_call["name"])
        if tool:
            result = tool.invoke(tool_call["args"])
            tool_results.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                    name=tool_call["name"],
                )
            )

    return {"messages": tool_results}


def should_continue(state: RecipeState) -> str:
    """Route: if tool calls exist → tool node; else → END."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END


# ── Graph ──────────────────────────────────────────────────────────────────────

def build_recipe_graph():
    graph = StateGraph(RecipeState)
    graph.add_node("model", recipe_model_node)
    graph.add_node("tools", recipe_tool_node)
    graph.set_entry_point("model")
    graph.add_conditional_edges("model", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "model")
    return graph.compile()


def run_recipe_agent(user_query: str) -> str:
    """Run the recipe agent and return the final text response."""
    app = build_recipe_graph()
    result = app.invoke({"messages": [HumanMessage(content=user_query)]})
    final_message = result["messages"][-1]

    if isinstance(final_message, AIMessage):
        return _normalize_content(final_message.content)

    return _normalize_content(getattr(final_message, "content", final_message))