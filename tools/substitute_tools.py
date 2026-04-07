from langchain_core.tools import tool


@tool
def find_ingredient_substitute(ingredient: str, reason: str = "") -> str:
    """
    Suggest substitutes for a missing or unavailable cooking ingredient.
    Provide the ingredient name and optionally why it's needed (e.g., allergy, unavailability).
    """
    substitutes = {
        "butter": [
            "🥑 Avocado (1:1 for baking) — creamy texture, healthier fats",
            "🥥 Coconut oil (3/4 cup per 1 cup butter) — adds subtle sweetness",
            "🍌 Mashed banana (1:1) — great for muffins and pancakes",
            "🫒 Olive oil (3/4 cup per 1 cup) — for sautéing and cooking",
            "🍎 Unsweetened applesauce (1:1) — for moist baked goods",
        ],
        "egg": [
            "🍌 1 mashed banana = 1 egg (for binding in baking)",
            "🌱 1 tbsp ground flaxseed + 3 tbsp water = 1 egg (flax egg)",
            "🫘 3 tbsp aquafaba (chickpea water) = 1 egg",
            "🥣 1/4 cup plain yogurt or buttermilk = 1 egg",
            "🍏 1/4 cup unsweetened applesauce = 1 egg (for moisture)",
        ],
        "milk": [
            "🥥 Coconut milk (1:1) — creamy and rich",
            "🌾 Almond milk (1:1) — lighter, slightly nutty flavor",
            "🫘 Soy milk (1:1) — closest in protein content",
            "🍚 Rice milk (1:1) — mild flavor, thinner consistency",
            "💧 Water + butter (7/8 cup water + 1 tbsp butter) — for cooking",
        ],
        "flour": [
            "🌾 Almond flour (1:1) — gluten-free, nutty taste",
            "🌽 Cornstarch (1 tbsp per 2 tbsp flour) — for thickening",
            "🍚 Rice flour (1:1) — gluten-free, light texture",
            "🫘 Chickpea flour (besan) — high protein, earthy flavor",
            "🥥 Oat flour — blend oats, use 1:1",
        ],
        "sugar": [
            "🍯 Honey (3/4 cup per 1 cup sugar) — reduce liquid by 1/4 cup",
            "🍁 Maple syrup (3/4 cup per 1 cup) — reduce other liquids",
            "🥥 Coconut sugar (1:1) — lower glycemic index",
            "🌱 Stevia (1 tsp per 1 cup) — zero calorie",
            "🍌 Mashed banana — natural sweetness for baking",
        ],
        "oil": [
            "🫒 Olive oil (1:1) — great for savory dishes",
            "🥥 Coconut oil (1:1) — adds flavor, solid at room temp",
            "🧈 Melted butter (1:1) — richer flavor",
            "🥑 Avocado oil (1:1) — high smoke point",
            "🍎 Applesauce (1:1) — for baking, reduces fat",
        ],
        "cream": [
            "🥥 Coconut cream (1:1) — dairy-free, thick",
            "🥛 Milk + butter (3/4 cup milk + 1/4 cup butter) = 1 cup cream",
            "🫘 Silken tofu (blended) — for soups and sauces",
            "🥜 Cashew cream (soaked cashews blended) — rich and creamy",
        ],
        "yogurt": [
            "🥛 Sour cream (1:1) — tangy, similar texture",
            "🍋 Buttermilk (1:1) — for marinades and baking",
            "🥥 Coconut yogurt (1:1) — dairy-free option",
            "🫘 Silken tofu (blended, 1:1) — smooth texture",
        ],
        "baking powder": [
            "🫧 1 tsp baking powder = 1/4 tsp baking soda + 1/2 tsp cream of tartar",
            "🥚 Beaten egg whites — for lift in cakes",
            "🍋 Baking soda + lemon juice (1/4 tsp + 1/2 tsp)",
        ],
        "lemon": [
            "🍊 Orange juice (1:1) — sweeter, less acidic",
            "🍷 White wine vinegar (1/2 tsp per 1 tsp lemon juice)",
            "🍇 Apple cider vinegar (1/2 tsp per 1 tsp lemon juice)",
            "🍋 Lime juice (1:1) — very similar flavor profile",
        ],
    }

    ingredient_lower = ingredient.lower().strip()

    # Check direct match first
    if ingredient_lower in substitutes:
        subs = substitutes[ingredient_lower]
        result = f"🔄 **Substitutes for {ingredient.title()}:**\n\n"
        for sub in subs:
            result += f"• {sub}\n"
        if reason:
            result += f"\n*Reason noted: {reason}*"
        result += "\n\n*Tip: Always adjust quantities based on your recipe's requirements.*"
        return result

    # Partial match
    for key, subs in substitutes.items():
        if key in ingredient_lower or ingredient_lower in key:
            result = f"🔄 **Substitutes for {ingredient.title()}:**\n\n"
            for sub in subs:
                result += f"• {sub}\n"
            result += "\n*Tip: Always adjust quantities based on your recipe's requirements.*"
            return result

    # Generic response
    return f"""
🔄 **Substitutes for {ingredient.title()}:**

I don't have a specific list for this ingredient, but here are general tips:

• **For binding**: Use flaxseed meal, chia seeds, or mashed banana
• **For moisture**: Use yogurt, applesauce, or plant milk
• **For fat**: Use avocado, nut butters, or coconut oil
• **For flavor**: Experiment with spices, herbs, or citrus zest
• **For leavening**: Use baking soda + acid (lemon/vinegar)

💡 *Try searching "{ingredient} substitute" on cooking websites like AllRecipes or Serious Eats for more specific options.*
"""


@tool
def get_pantry_alternatives(dish_name: str, missing_ingredients: str) -> str:
    """
    Suggest how to adapt a dish when certain ingredients are missing.
    Provide the dish name and a comma-separated list of missing ingredients.
    """
    missing_list = [i.strip() for i in missing_ingredients.split(",")]

    result = f"🍳 **Adapting '{dish_name}' without: {', '.join(missing_list)}**\n\n"

    for ingredient in missing_list:
        result += f"**Without {ingredient}:**\n"
        sub_tool_result = find_ingredient_substitute.invoke(
            {"ingredient": ingredient, "reason": f"for making {dish_name}"}
        )
        # Extract just the substitute lines
        lines = sub_tool_result.split("\n")
        subs = [l for l in lines if l.strip().startswith("•")][:3]
        for sub in subs:
            result += f"  {sub}\n"
        result += "\n"

    result += "✅ *With these swaps, your dish should still turn out delicious!*"
    return result
