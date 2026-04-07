"""
Ingredient Substitute Agent — Modern Prebuilt LangChain Agent
Suggests smart ingredient alternatives using tool-augmented Gemini.
"""

from langchain.agents import create_agent

from config.settings import get_llm
from tools.substitute_tools import find_ingredient_substitute, get_pantry_alternatives


# ── Tools ──────────────────────────────────────────────────────────────────────

SUBSTITUTE_TOOLS = [find_ingredient_substitute, get_pantry_alternatives]


# ── System Prompt ──────────────────────────────────────────────────────────────

SUBSTITUTE_SYSTEM_PROMPT = """
You are ChefMate AI's Ingredient Substitute Expert — a creative culinary assistant
who helps home cooks adapt recipes when they're missing ingredients.

Your expertise:
- Use the available tools whenever relevant
- Use find_ingredient_substitute for specific ingredient queries
- Use get_pantry_alternatives when multiple ingredients are missing for a dish
- Explain why each substitute works based on flavor, texture, or cooking function
- Mention any quantity or technique adjustments if needed
- Consider dietary restrictions such as vegan, lactose-free, and gluten-free
- Prioritize affordable, easy-to-find alternatives

Always be creative, practical, and reassuring — cooking with substitutes can be fun.
""".strip()


# ── Response Normalizer ────────────────────────────────────────────────────────

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


# ── Agent Builder ──────────────────────────────────────────────────────────────

def build_substitute_agent():
    """Build and return the substitute agent."""
    llm = get_llm(temperature=0.4)

    agent = create_agent(
        model=llm,
        tools=SUBSTITUTE_TOOLS,
        system_prompt=SUBSTITUTE_SYSTEM_PROMPT,
    )
    return agent


def run_substitute_agent(user_query: str) -> str:
    """Run the substitute agent and return the response."""
    try:
        agent = build_substitute_agent()

        result = agent.invoke({
            "messages": [
                {"role": "user", "content": user_query}
            ]
        })

        messages = result.get("messages", [])
        if messages:
            last_message = messages[-1]
            if hasattr(last_message, "content") and last_message.content:
                return _normalize_content(last_message.content)

        return "I couldn't find substitutes. Please try again."

    except Exception as e:
        return f"⚠️ Substitute Agent error: {str(e)}"