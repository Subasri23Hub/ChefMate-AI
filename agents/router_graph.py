"""
Router Agent — LangGraph-based query router
Automatically classifies user queries and routes them to the correct agent.
"""

from typing import Annotated, TypedDict, Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage

from config.settings import get_llm

# ── Agent imports ──────────────────────────────────────────────────────────────
from agents.recipe_graph import run_recipe_agent
from agents.meal_planner_graph import run_meal_planner_agent
from agents.nutrition_agent import run_nutrition_agent
from agents.substitute_agent import run_substitute_agent


# ── State ──────────────────────────────────────────────────────────────────────

class RouterState(TypedDict):
    messages: Annotated[list, add_messages]
    route: str
    final_response: str


# ── Classification Prompt ──────────────────────────────────────────────────────

ROUTER_SYSTEM_PROMPT = """
You are a query router for ChefMate AI. Classify the user's message into exactly ONE category:

- "recipe"    → user wants a specific recipe, cooking instructions, or "how to make X"
- "planner"   → user wants a meal plan, diet plan, weekly/daily food schedule
- "nutrition" → user wants food suggestions, what to eat for a goal, healthy food advice
- "substitute"→ user doesn't have an ingredient, wants alternatives or replacements

Respond with ONLY the category word: recipe, planner, nutrition, or substitute.
No explanation. No punctuation. Just the single word.
"""


# ── Router Node ────────────────────────────────────────────────────────────────

def router_node(state: RouterState) -> dict:
    """Classify the user query into an agent route."""
    llm = get_llm(temperature=0.0)
    user_message = state["messages"][-1].content

    response = llm.invoke([
        SystemMessage(content=ROUTER_SYSTEM_PROMPT),
        HumanMessage(content=user_message),
    ])

    route = response.content.strip().lower()
    if route not in ("recipe", "planner", "nutrition", "substitute"):
        route = "nutrition"  # safe fallback

    return {"route": route}


# ── Agent Execution Nodes ──────────────────────────────────────────────────────

def execute_recipe(state: RouterState) -> dict:
    query = state["messages"][-1].content
    return {"final_response": run_recipe_agent(query)}


def execute_planner(state: RouterState) -> dict:
    query = state["messages"][-1].content
    return {"final_response": run_meal_planner_agent(query)}


def execute_nutrition(state: RouterState) -> dict:
    query = state["messages"][-1].content
    return {"final_response": run_nutrition_agent(query)}


def execute_substitute(state: RouterState) -> dict:
    query = state["messages"][-1].content
    return {"final_response": run_substitute_agent(query)}


# ── Routing Logic ──────────────────────────────────────────────────────────────

def route_to_agent(state: RouterState) -> Literal["recipe", "planner", "nutrition", "substitute"]:
    return state["route"]


# ── Graph ──────────────────────────────────────────────────────────────────────

def build_router_graph() -> StateGraph:
    graph = StateGraph(RouterState)

    graph.add_node("router", router_node)
    graph.add_node("recipe", execute_recipe)
    graph.add_node("planner", execute_planner)
    graph.add_node("nutrition", execute_nutrition)
    graph.add_node("substitute", execute_substitute)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        route_to_agent,
        {
            "recipe": "recipe",
            "planner": "planner",
            "nutrition": "nutrition",
            "substitute": "substitute",
        },
    )

    graph.add_edge("recipe", END)
    graph.add_edge("planner", END)
    graph.add_edge("nutrition", END)
    graph.add_edge("substitute", END)

    return graph.compile()


def run_router_agent(user_query: str) -> tuple[str, str]:
    """
    Run the router agent.
    Returns (agent_type, response_text) tuple.
    """
    app = build_router_graph()
    result = app.invoke({
        "messages": [HumanMessage(content=user_query)],
        "route": "",
        "final_response": "",
    })
    return result["route"], result["final_response"]
