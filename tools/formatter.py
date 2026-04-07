def format_recipe_card(recipe_data: dict) -> str:
    """Format recipe data into a clean markdown string."""
    if not recipe_data.get("found"):
        return f"⚠️ {recipe_data.get('message', 'Recipe not found.')}"

    ingredients_text = "\n".join(
        [f"• {ing}" for ing in recipe_data.get("ingredients", [])]
    )

    instructions = recipe_data.get("instructions", "")
    # Break instructions into numbered steps
    steps = [s.strip() for s in instructions.split("\r\n") if s.strip()]
    if len(steps) <= 2:
        steps = [s.strip() for s in instructions.split("\n") if s.strip()]

    numbered_steps = "\n".join(
        [f"{i+1}. {step}" for i, step in enumerate(steps[:15])]
    )

    card = f"""
## 🍽️ {recipe_data.get('title', 'Recipe')}

**Cuisine:** {recipe_data.get('cuisine', 'International')} | **Category:** {recipe_data.get('category', 'General')}

---

### 📋 Ingredients
{ingredients_text}

---

### 👨‍🍳 Instructions
{numbered_steps}
"""

    if recipe_data.get("youtube_url"):
        card += f"\n🎥 [Watch on YouTube]({recipe_data['youtube_url']})"

    if recipe_data.get("source_url"):
        card += f" | 🔗 [Original Recipe]({recipe_data['source_url']})"

    return card


def format_meal_plan(plan_text: str) -> str:
    """Clean and format meal plan output."""
    return plan_text.strip()


def truncate_text(text: str, max_chars: int = 500) -> str:
    """Truncate text with ellipsis if too long."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "..."
