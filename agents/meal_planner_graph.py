"""
Meal Planner Agent — Custom LangGraph Agent
Generates structured meal plans using Gemini's reasoning capabilities.
"""

from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from config.settings import get_llm


# ── State ──────────────────────────────────────────────────────────────────────

class MealPlannerState(TypedDict):
    messages: Annotated[list, add_messages]


# ── System Prompt ──────────────────────────────────────────────────────────────

MEAL_PLANNER_SYSTEM_PROMPT = """
You are ChefMate AI's professional Meal Planner Agent. Your task is to create detailed,
nutritionally balanced, and practical meal plans.

When generating a meal plan, always include:
1. A clear title (e.g., "🗓️ 7-Day Healthy Meal Plan")
2. Each day broken down into: Breakfast, Mid-Morning Snack, Lunch, Evening Snack, Dinner
3. Estimated calories per day
4. Nutritional highlights (proteins, carbs, fats)
5. Practical cooking tips
6. A shopping list summary at the end

Format the plan cleanly using markdown with emojis for readability.
Consider: dietary restrictions, health goals, budget, cuisine preferences, and local ingredients.
Tailor the plan specifically to Indian/South Asian food preferences when not specified.

Be specific with quantities (e.g., "2 chapatis", "1 cup cooked dal", "100g chicken").
"""


# ── Nodes ──────────────────────────────────────────────────────────────────────

def planner_model_node(state: MealPlannerState):
    """Core planning node — uses Gemini to generate meal plans."""
    llm = get_llm(temperature=0.6)
    messages = [SystemMessage(content=MEAL_PLANNER_SYSTEM_PROMPT)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def refine_plan_node(state: MealPlannerState):
    """Optional refinement node — adds shopping list if missing."""
    last_message = state["messages"][-1]
    content = last_message.content if isinstance(last_message, AIMessage) else ""

    if "shopping list" not in content.lower() and "grocery" not in content.lower():
        llm = get_llm(temperature=0.3)
        refinement_prompt = (
            f"Based on this meal plan:\n\n{content}\n\n"
            "Please add a concise 'Shopping List' section at the end, "
            "grouping items by: Vegetables, Fruits, Grains & Cereals, "
            "Protein Sources, Dairy, Spices & Condiments."
        )
        refined = llm.invoke([HumanMessage(content=refinement_prompt)])
        return {"messages": [refined]}

    return {"messages": []}


def should_refine(state: MealPlannerState) -> str:
    """Route: always refine for completeness."""
    return "refine"


# ── Graph ──────────────────────────────────────────────────────────────────────

def build_meal_planner_graph() -> StateGraph:
    graph = StateGraph(MealPlannerState)
    graph.add_node("planner", planner_model_node)
    graph.add_node("refine", refine_plan_node)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "refine")
    graph.add_edge("refine", END)
    return graph.compile()


def run_meal_planner_agent(user_query: str) -> str:
    """Run the meal planner agent and return the final plan."""
    app = build_meal_planner_graph()
    result = app.invoke({"messages": [HumanMessage(content=user_query)]})
    final_message = result["messages"][-1]

    if isinstance(final_message, AIMessage):
        return final_message.content
    return str(final_message.content) if hasattr(final_message, "content") else "Could not generate meal plan."
