"""
UI Components — Reusable Streamlit UI elements for ChefMate AI
"""

import streamlit as st


# ── Constants ──────────────────────────────────────────────────────────────────

AGENT_META = {
    "recipe": {
        "icon": "🍽️",
        "label": "Recipe Agent",
        "color": "#FF6B35",
        "desc": "Find recipes & cooking instructions",
        "badge_color": "#FF6B35",
    },
    "planner": {
        "icon": "🗓️",
        "label": "Meal Planner",
        "color": "#4ECDC4",
        "desc": "Generate weekly/daily meal plans",
        "badge_color": "#4ECDC4",
    },
    "nutrition": {
        "icon": "🥗",
        "label": "Nutrition Advisor",
        "color": "#45B7D1",
        "desc": "Personalized food & health advice",
        "badge_color": "#45B7D1",
    },
    "substitute": {
        "icon": "🔄",
        "label": "Ingredient Substitute",
        "color": "#96CEB4",
        "desc": "Smart ingredient alternatives",
        "badge_color": "#96CEB4",
    },
}

AGENT_OPTIONS = {
    "🤖 Auto-Route (Smart)": "auto",
    "🍽️ Recipe Agent": "recipe",
    "🗓️ Meal Planner": "planner",
    "🥗 Nutrition Advisor": "nutrition",
    "🔄 Ingredient Substitute": "substitute",
}

EXAMPLE_PROMPTS = {
    "recipe": [
        "Give me a recipe for butter chicken",
        "How to make chocolate lava cake?",
        "Show me a pasta recipe",
        "Recipe for masala dosa",
        "Surprise me with a random recipe 🎲",
    ],
    "planner": [
        "Create a 7-day healthy meal plan",
        "Give me a 1-day vegetarian diet plan",
        "Plan a high-protein meal schedule for muscle gain",
        "Low-calorie meal plan for weight loss",
        "Diabetic-friendly 3-day meal plan",
    ],
    "nutrition": [
        "What should I eat for weight loss?",
        "Suggest a healthy breakfast for me",
        "Foods to eat for better energy",
        "What to eat for diabetes management?",
        "Best foods for muscle building",
    ],
    "substitute": [
        "I don't have butter, what can I use?",
        "Substitute for eggs in baking?",
        "What can replace milk in a recipe?",
        "I'm out of baking powder",
        "Vegan substitute for cream",
    ],
}


# ── Sidebar ────────────────────────────────────────────────────────────────────

def render_sidebar() -> tuple[str, bool]:
    """
    Render the sidebar with branding, agent selection, and examples.
    Returns (selected_agent_key, show_examples).
    """
    with st.sidebar:
        # Logo / Branding
        st.markdown(
            """
            <div style="text-align:center; padding: 1rem 0 0.5rem 0;">
                <div style="font-size: 3rem;">👨‍🍳</div>
                <h1 style="
                    font-size: 1.8rem;
                    font-weight: 800;
                    background: linear-gradient(135deg, #FF6B35, #F7931E);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin: 0;
                ">ChefMate AI</h1>
                <p style="font-size: 0.75rem; color: #888; margin-top: 0.2rem;">
                    Your AI Food Intelligence Assistant
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                border-left: 3px solid #FF6B35;
                padding: 0.8rem 1rem;
                border-radius: 0 8px 8px 0;
                margin: 0.5rem 0 1rem 0;
                font-size: 0.8rem;
                color: #ccc;
                font-style: italic;
            ">
                "AI has no age limit. It can assist anyone, anywhere, in everyday life."
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### 🤖 Select Agent")
        selected_label = st.selectbox(
            "Agent Mode",
            options=list(AGENT_OPTIONS.keys()),
            index=0,
            label_visibility="collapsed",
        )
        selected_agent = AGENT_OPTIONS[selected_label]

        st.markdown("---")

        # Agent info cards
        if selected_agent == "auto":
            st.markdown("**✨ Auto-Route Mode**")
            st.markdown(
                "<small style='color:#aaa'>The smart router will automatically detect "
                "your intent and send your query to the best agent.</small>",
                unsafe_allow_html=True,
            )
        else:
            meta = AGENT_META.get(selected_agent, {})
            st.markdown(
                f"""
                <div style="
                    background: #1a1a2e;
                    border: 1px solid {meta.get('color','#555')};
                    border-radius: 8px;
                    padding: 0.7rem;
                    margin-bottom: 0.5rem;
                ">
                    <span style="font-size:1.3rem">{meta.get('icon','')}</span>
                    <strong style="color:{meta.get('color','#fff')}">{meta.get('label','')}</strong><br>
                    <small style="color:#aaa">{meta.get('desc','')}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # Example prompts
        st.markdown("### 💡 Example Prompts")
        example_key = selected_agent if selected_agent != "auto" else "recipe"
        examples = EXAMPLE_PROMPTS.get(example_key, EXAMPLE_PROMPTS["recipe"])

        show_examples = st.toggle("Show examples", value=True)
        if show_examples:
            for ex in examples:
                if st.button(ex, key=f"ex_{ex[:20]}", use_container_width=True):
                    st.session_state["prefill_input"] = ex

        st.markdown("---")

        # Stats in sidebar
        if "chat_history" in st.session_state:
            total = len(st.session_state.chat_history)
            st.markdown(
                f"<small style='color:#888'>💬 {total} message{'s' if total != 1 else ''} this session</small>",
                unsafe_allow_html=True,
            )

        # Clear button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.pop("prefill_input", None)
            st.rerun()

        st.markdown(
            "<div style='text-align:center;margin-top:1rem;color:#555;font-size:0.7rem'>"
            "Powered by Gemini 2.5 Flash + LangGraph<br>"
            "© 2025 ChefMate AI"
            "</div>",
            unsafe_allow_html=True,
        )

    return selected_agent, show_examples


# ── Hero Header ────────────────────────────────────────────────────────────────

def render_hero():
    """Render the main page hero section."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
            border-radius: 16px;
            padding: 2rem 2rem 1.5rem 2rem;
            margin-bottom: 1.5rem;
            border: 1px solid #2a2a4a;
            text-align: center;
        ">
            <div style="font-size:3rem; margin-bottom:0.5rem">👨‍🍳</div>
            <h1 style="
                font-size:2.5rem;
                font-weight:900;
                background: linear-gradient(135deg, #FF6B35 0%, #F7931E 50%, #FFD700 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin:0 0 0.4rem 0;
            ">ChefMate AI</h1>
            <p style="color:#aaa; font-size:1rem; margin:0 0 1rem 0;">
                Your intelligent food assistant — powered by Gemini 2.5 Flash & LangGraph
            </p>
            <div style="display:flex; justify-content:center; gap:0.5rem; flex-wrap:wrap;">
                <span style="background:#FF6B3520;color:#FF6B35;padding:0.25rem 0.7rem;border-radius:20px;font-size:0.75rem;border:1px solid #FF6B3540">🍽️ Recipes</span>
                <span style="background:#4ECDC420;color:#4ECDC4;padding:0.25rem 0.7rem;border-radius:20px;font-size:0.75rem;border:1px solid #4ECDC440">🗓️ Meal Plans</span>
                <span style="background:#45B7D120;color:#45B7D1;padding:0.25rem 0.7rem;border-radius:20px;font-size:0.75rem;border:1px solid #45B7D140">🥗 Nutrition</span>
                <span style="background:#96CEB420;color:#96CEB4;padding:0.25rem 0.7rem;border-radius:20px;font-size:0.75rem;border:1px solid #96CEB440">🔄 Substitutes</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Agent Badge ────────────────────────────────────────────────────────────────

def render_agent_badge(agent_type: str):
    """Render a colored badge showing which agent responded."""
    meta = AGENT_META.get(agent_type, {
        "icon": "🤖", "label": "AI Agent", "color": "#888"
    })
    st.markdown(
        f"""
        <div style="
            display:inline-flex;
            align-items:center;
            gap:0.4rem;
            background:{meta['color']}20;
            color:{meta['color']};
            border:1px solid {meta['color']}40;
            border-radius:20px;
            padding:0.2rem 0.8rem;
            font-size:0.78rem;
            font-weight:600;
            margin-bottom:0.5rem;
        ">
            {meta['icon']} {meta['label']} responded
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Recipe Image Card ──────────────────────────────────────────────────────────

def render_recipe_image(image_url: str, title: str):
    """Render a recipe image with caption if URL is present."""
    if image_url and image_url.startswith("http"):
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.image(image_url, caption=f"🍽️ {title}", use_container_width=True)


# ── Response Card ──────────────────────────────────────────────────────────────

def render_response_card(content: str, agent_type: str = ""):
    """Render the AI response in a styled card."""
    if agent_type:
        render_agent_badge(agent_type)
    st.markdown(content)


# ── Chat Message ───────────────────────────────────────────────────────────────

def render_chat_message(role: str, content: str, agent_type: str = ""):
    """Render a single chat message bubble."""
    if role == "user":
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(content)
    else:
        with st.chat_message("assistant", avatar="👨‍🍳"):
            render_response_card(content, agent_type)


# ── Welcome Screen ─────────────────────────────────────────────────────────────

def render_welcome():
    """Render the welcome / empty state screen."""
    st.markdown(
        """
        <div style="
            text-align:center;
            padding: 3rem 1rem;
            color: #555;
        ">
            <div style="font-size:4rem; margin-bottom:1rem">🍳</div>
            <h3 style="color:#777; font-weight:600">What would you like help with today?</h3>
            <p style="color:#555; font-size:0.9rem">
                Ask me anything about food — I'll find recipes, plan your meals,<br>
                give nutrition advice, or suggest ingredient substitutes.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(2)
    quick_starts = [
        ("🍽️", "Recipe", "Give me a recipe for biryani"),
        ("🗓️", "Meal Plan", "Create a 7-day healthy meal plan"),
        ("🥗", "Nutrition", "What should I eat for weight loss?"),
        ("🔄", "Substitute", "I don't have butter, what can I use?"),
    ]
    for i, (icon, label, prompt) in enumerate(quick_starts):
        with cols[i % 2]:
            if st.button(f"{icon} {label}\n\n*\"{prompt[:35]}...\"*",
                         key=f"quick_{i}", use_container_width=True):
                st.session_state["prefill_input"] = prompt
                st.rerun()


# ── Error Card ─────────────────────────────────────────────────────────────────

def render_error(message: str):
    """Display a styled error message."""
    st.markdown(
        f"""
        <div style="
            background: #2d0a0a;
            border: 1px solid #ff4444;
            border-radius: 8px;
            padding: 1rem;
            color: #ff8080;
        ">
            ⚠️ <strong>Oops!</strong> {message}
        </div>
        """,
        unsafe_allow_html=True,
    )
