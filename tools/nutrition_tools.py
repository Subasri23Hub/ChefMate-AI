from langchain_core.tools import tool


@tool
def get_nutrition_advice(goal: str, preferences: str = "") -> str:
    """
    Provide nutrition advice based on health goals.
    Goals can include: weight loss, muscle gain, diabetes management,
    heart health, energy boost, healthy eating, etc.
    """
    advice_map = {
        "weight loss": """
🥗 **Weight Loss Nutrition Plan**
- **Breakfast**: Oats with berries, green tea, boiled eggs
- **Mid-Morning**: Apple or handful of almonds
- **Lunch**: Brown rice / chapati + dal + salad + curd
- **Evening**: Sprouts chaat or vegetable soup
- **Dinner**: Grilled fish/paneer + steamed vegetables
- **Key Tips**: Eat every 3–4 hours, stay hydrated (2–3L water), avoid processed sugar
""",
        "muscle gain": """
💪 **Muscle Gain Nutrition Plan**
- **Breakfast**: 4 eggs + whole wheat toast + banana + milk
- **Mid-Morning**: Protein shake + peanut butter
- **Lunch**: Chicken/paneer + brown rice + dal + salad
- **Post-Workout**: Whey protein + banana
- **Dinner**: Salmon/tofu + sweet potato + vegetables
- **Key Tips**: Protein at every meal, caloric surplus, strength training
""",
        "diabetes": """
🩺 **Diabetes-Friendly Nutrition**
- **Breakfast**: Methi paratha + curd or vegetable oats
- **Mid-Morning**: Guava or handful of walnuts
- **Lunch**: Bajra/jowar roti + palak dal + salad
- **Evening**: Roasted chana or cucumber slices
- **Dinner**: Mixed vegetable curry + small portion brown rice
- **Key Tips**: Low GI foods, avoid refined carbs, regular small meals
""",
        "heart health": """
❤️ **Heart-Healthy Nutrition**
- **Breakfast**: Oatmeal + flaxseeds + mixed berries
- **Lunch**: Grilled fish + quinoa + leafy greens
- **Snack**: Walnuts + dark chocolate (70%+)
- **Dinner**: Lentil soup + whole grain bread + salad
- **Key Tips**: Omega-3 fatty acids, reduce sodium, avoid trans fats
""",
        "energy": """
⚡ **Energy Boosting Nutrition**
- **Breakfast**: Banana + peanut butter toast + black coffee
- **Mid-Morning**: Dates + mixed nuts
- **Lunch**: Rice + sambar + vegetables + curd
- **Evening**: Fruit smoothie with seeds
- **Dinner**: Quinoa/millets + grilled protein + veggies
- **Key Tips**: Complex carbs throughout day, stay hydrated, iron-rich foods
""",
    }

    goal_lower = goal.lower()
    for key, advice in advice_map.items():
        if key in goal_lower:
            return advice

    # Default healthy eating advice
    return f"""
🌿 **Healthy Eating Advice for: {goal}**

**Balanced Daily Plate:**
- 50% vegetables and fruits
- 25% whole grains (brown rice, oats, millets)
- 25% lean protein (dal, eggs, chicken, paneer)
- Healthy fats (olive oil, nuts, seeds)

**Smart Choices:**
- Drink 8–10 glasses of water daily
- Eat 4–5 small meals instead of 2–3 large ones
- Include seasonal and local foods
- Minimize processed foods, salt, and added sugar
- Add fermented foods for gut health (curd, idli, dosa)

**Foods to Include:**
- Fruits: Banana, papaya, pomegranate, guava
- Vegetables: Spinach, tomato, carrot, broccoli
- Grains: Oats, brown rice, millets
- Protein: Lentils, eggs, paneer, fish

*Consult a registered dietitian for a personalized plan.*
"""


@tool
def suggest_healthy_breakfast(dietary_preference: str = "any") -> str:
    """
    Suggest healthy breakfast options based on dietary preference.
    Options: vegetarian, vegan, non-vegetarian, any
    """
    options = {
        "vegetarian": [
            "🥣 Oats with banana, honey, and mixed seeds",
            "🫓 Whole wheat toast with avocado and boiled eggs",
            "🥞 Ragi/finger millet dosa with coconut chutney",
            "🍲 Poha with vegetables, peanuts, and lemon",
            "🥛 Greek yogurt parfait with granola and berries",
        ],
        "vegan": [
            "🥑 Smoothie bowl with plant milk, berries, and chia seeds",
            "🌾 Overnight oats with almond milk and fruits",
            "🫘 Sprouts salad with lemon, coriander, and tomato",
            "🍌 Banana pancakes (oats + banana + flaxseed)",
            "🥣 Millet porridge with coconut milk and nuts",
        ],
        "non-vegetarian": [
            "🥚 Scrambled eggs with whole grain toast and avocado",
            "🐟 Grilled salmon with oats and orange juice",
            "🍳 Omelette with vegetables and a glass of milk",
            "🥩 Turkey wrap with lettuce, tomato, and hummus",
            "🍗 Chicken poha or egg bhurji with chapati",
        ],
    }

    pref = dietary_preference.lower()
    if pref in options:
        meals = options[pref]
    else:
        meals = options["vegetarian"] + options["non-vegetarian"][:2]

    result = f"🌅 **Healthy Breakfast Options ({dietary_preference.title()}):**\n\n"
    for meal in meals[:5]:
        result += f"• {meal}\n"
    result += "\n*Aim for a breakfast with protein + complex carbs + healthy fats.*"
    return result
