"""
ChefMate AI — Main Streamlit Application
Multi-Agent AI Food Intelligence Assistant
Built with LangGraph + Gemini 2.5 Flash
"""

import streamlit as st
import re

# ── Page Config (must be first Streamlit call) ─────────────────────────────────
st.set_page_config(
    page_title="ChefMate AI",
    page_icon="👨‍🍳",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "ChefMate AI — Your AI-powered Food Intelligence Assistant",
    },
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Base & Background ── */
    .stApp {
        background: #0d0d1a;
        color: #e0e0e0;
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #0f0f1e !important;
        border-right: 1px solid #2a2a4a;
    }
    [data-testid="stSidebar"] .stButton button {
        background: #1a1a2e;
        color: #ccc;
        border: 1px solid #2a2a4a;
        border-radius: 8px;
        font-size: 0.8rem;
        text-align: left;
        transition: all 0.2s ease;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background: #FF6B3520;
        border-color: #FF6B35;
        color: #FF6B35;
    }

    /* ── Chat Messages ── */
    [data-testid="stChatMessage"] {
        background: #131320;
        border: 1px solid #2a2a4a;
        border-radius: 12px;
        margin-bottom: 0.75rem;
        padding: 0.5rem;
    }

    /* ── Chat Input ── */
    [data-testid="stChatInput"] {
        background: #131320 !important;
        border: 1px solid #2a2a4a !important;
        border-radius: 12px !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #e0e0e0 !important;
    }

    /* ── Buttons ── */
    .stButton button {
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        background: #1a1a2e !important;
        border-color: #2a2a4a !important;
        color: #e0e0e0 !important;
    }

    /* ── Spinner ── */
    .stSpinner > div {
        border-color: #FF6B35 transparent transparent transparent !important;
    }

    /* ── Markdown ── */
    h1, h2, h3 { color: #f0f0f0 !important; }
    hr { border-color: #2a2a4a !important; }
    code { background: #1a1a2e !important; color: #FF6B35 !important; }
    blockquote { border-left-color: #FF6B35 !important; }

    /* ── Toggle ── */
    .stToggle { color: #aaa !important; }

    /* ── Sidebar reopen fix ONLY ── */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    [data-testid="collapsedControl"] {
        color: #FF6B35 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Imports (after page config) ────────────────────────────────────────────────
from ui.components import (
    render_sidebar,
    render_hero,
    render_chat_message,
    render_welcome,
    render_error,
    render_recipe_image,
)
from agents.recipe_graph import run_recipe_agent
from agents.meal_planner_graph import run_meal_planner_agent
from agents.nutrition_agent import run_nutrition_agent
from agents.substitute_agent import run_substitute_agent
from agents.router_graph import run_router_agent


# ── Session State ──────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "prefill_input" not in st.session_state:
    st.session_state.prefill_input = ""


# ── Agent Dispatcher ───────────────────────────────────────────────────────────
def dispatch_query(query: str, agent_mode: str) -> tuple[str, str]:
    """
    Dispatch a query to the appropriate agent.
    Returns (agent_type, response_text).
    """
    if agent_mode == "auto":
        return run_router_agent(query)
    elif agent_mode == "recipe":
        return "recipe", run_recipe_agent(query)
    elif agent_mode == "planner":
        return "planner", run_meal_planner_agent(query)
    elif agent_mode == "nutrition":
        return "nutrition", run_nutrition_agent(query)
    elif agent_mode == "substitute":
        return "substitute", run_substitute_agent(query)
    else:
        return "nutrition", run_nutrition_agent(query)


def extract_image_url(response_text: str) -> str | None:
    """Extract a MealDB image URL from response text if present."""
    pattern = r"https://www\.themealdb\.com/images/media/meals/[^\s\)\]\"']+"
    match = re.search(pattern, response_text)
    return match.group(0) if match else None


def extract_title(response_text: str) -> str:
    """Try to extract a recipe title from the response."""
    match = re.search(r"##\s+🍽️\s+(.+)", response_text)
    return match.group(1).strip() if match else "Recipe"


# ── Sidebar ────────────────────────────────────────────────────────────────────
selected_agent, _ = render_sidebar()

# ── Main Layout ────────────────────────────────────────────────────────────────
render_hero()

# ── Chat History ───────────────────────────────────────────────────────────────
if not st.session_state.chat_history:
    render_welcome()
else:
    for msg in st.session_state.chat_history:
        render_chat_message(
            role=msg["role"],
            content=msg["content"],
            agent_type=msg.get("agent_type", ""),
        )
        # Show recipe image if available
        if msg["role"] == "assistant" and msg.get("image_url"):
            render_recipe_image(msg["image_url"], msg.get("recipe_title", "Recipe"))

# ── Chat Input ─────────────────────────────────────────────────────────────────
prefill = st.session_state.pop("prefill_input", "")

user_input = st.chat_input(
    placeholder="Ask me about recipes, meal plans, nutrition, or ingredient substitutes...",
    key="main_chat_input",
)

# Use prefill if no direct input
if prefill and not user_input:
    user_input = prefill

# ── Process Query ──────────────────────────────────────────────────────────────
if user_input and user_input.strip():
    query = user_input.strip()

    # Display user message immediately
    st.session_state.chat_history.append({"role": "user", "content": query})
    render_chat_message("user", query)

    # Spinner while agent processes
    with st.spinner("🤔 ChefMate is thinking..."):
        try:
            agent_type, response = dispatch_query(query, selected_agent)

            # Extract image URL if recipe response
            image_url = None
            recipe_title = ""
            if agent_type == "recipe":
                image_url = extract_image_url(response)
                recipe_title = extract_title(response)

            # Store in history
            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": response,
                    "agent_type": agent_type,
                    "image_url": image_url,
                    "recipe_title": recipe_title,
                }
            )

            # Display response
            render_chat_message("assistant", response, agent_type)
            if image_url:
                render_recipe_image(image_url, recipe_title)

        except Exception as e:
            error_msg = str(e)
            if "API_KEY" in error_msg or "api_key" in error_msg:
                render_error(
                    "Invalid or missing Gemini API key. "
                    "Please add your GOOGLE_API_KEY to the .env file."
                )
            else:
                render_error(f"Something went wrong: {error_msg}")

    st.rerun()