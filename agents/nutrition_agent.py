"""
Nutrition Advisor Agent — Modern Prebuilt LangChain Agent
Provides personalized nutrition advice using tool-augmented Gemini.
"""

from langchain.agents import create_agent

from config.settings import get_llm
from tools.nutrition_tools import get_nutrition_advice, suggest_healthy_breakfast


# ── Tools ──────────────────────────────────────────────────────────────────────

NUTRITION_TOOLS = [get_nutrition_advice, suggest_healthy_breakfast]


# ── System Prompt ──────────────────────────────────────────────────────────────

NUTRITION_SYSTEM_PROMPT = """
You are ChefMate AI's Nutrition Advisor — a warm, knowledgeable, and supportive
nutrition assistant. Your role is to guide users toward healthier eating habits.

Your approach:
- Always use the available tools whenever they are relevant
- Be encouraging and non-judgmental
- Consider the user's lifestyle, culture, and preferences
- Provide practical, actionable suggestions
- Recommend Indian/South Asian food options where relevant
- Always end with a motivational tip or reminder

When asked about what to eat, healthy routines, breakfast suggestions, or diet support,
use the available nutrition tools if they help give a better answer.
Be specific, warm, and helpful.
""".strip()


# ── Agent Builder ──────────────────────────────────────────────────────────────

def build_nutrition_agent():
    """Build and return the nutrition advisor agent."""
    llm = get_llm(temperature=0.5)

    agent = create_agent(
        model=llm,
        tools=NUTRITION_TOOLS,
        system_prompt=NUTRITION_SYSTEM_PROMPT,
    )
    return agent


def run_nutrition_agent(user_query: str) -> str:
    """Run the nutrition agent and return the response."""
    try:
        agent = build_nutrition_agent()
        result = agent.invoke({
            "messages": [
                {"role": "user", "content": user_query}
            ]
        })

        messages = result.get("messages", [])
        if messages:
            last_message = messages[-1]
            if hasattr(last_message, "content"):
                return last_message.content or "I couldn't generate nutrition advice. Please try again."

        return "I couldn't generate nutrition advice. Please try again."

    except Exception as e:
        return f"⚠️ Nutrition Agent error: {str(e)}"