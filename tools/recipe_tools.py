import requests
from langchain_core.tools import tool


MEALDB_BASE_URL = "https://www.themealdb.com/api/json/v1/1"


@tool
def search_recipe_by_name(meal_name: str) -> str:
    """
    Search for a recipe by meal name using TheMealDB API.
    Returns formatted recipe details including title, image, category, cuisine,
    ingredients, and instructions.
    """
    try:
        url = f"{MEALDB_BASE_URL}/search.php"
        response = requests.get(url, params={"s": meal_name}, timeout=10)
        response.raise_for_status()
        data = response.json()

        meals = data.get("meals")
        if not meals:
            return f"No recipe found for '{meal_name}'. Try a different name."

        meal = meals[0]

        ingredients = []
        for i in range(1, 21):
            ingredient = (meal.get(f"strIngredient{i}") or "").strip()
            measure = (meal.get(f"strMeasure{i}") or "").strip()
            if ingredient:
                ingredients.append(
                    f"- {measure} {ingredient}".strip() if measure else f"- {ingredient}"
                )

        ingredients_text = "\n".join(ingredients) if ingredients else "Not available"

        return f"""## 🍽️ {meal.get("strMeal", "")}

**Category:** {meal.get("strCategory", "")}
**Cuisine:** {meal.get("strArea", "")}

**Ingredients:**
{ingredients_text}

**Instructions:**
{meal.get("strInstructions", "")}

**Image URL:** {meal.get("strMealThumb", "")}
**YouTube:** {meal.get("strYoutube", "")}
**Source:** {meal.get("strSource", "")}
"""

    except requests.RequestException as e:
        return f"API error: {str(e)}"


@tool
def get_random_recipe() -> str:
    """
    Fetch a random recipe from TheMealDB API.
    Useful when user asks for a surprise or random meal suggestion.
    """
    try:
        url = f"{MEALDB_BASE_URL}/random.php"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        meal = data["meals"][0]

        ingredients = []
        for i in range(1, 21):
            ingredient = (meal.get(f"strIngredient{i}") or "").strip()
            measure = (meal.get(f"strMeasure{i}") or "").strip()
            if ingredient:
                ingredients.append(
                    f"- {measure} {ingredient}".strip() if measure else f"- {ingredient}"
                )

        ingredients_text = "\n".join(ingredients) if ingredients else "Not available"

        return f"""## 🍽️ {meal.get("strMeal", "")}

**Category:** {meal.get("strCategory", "")}
**Cuisine:** {meal.get("strArea", "")}

**Ingredients:**
{ingredients_text}

**Instructions:**
{meal.get("strInstructions", "")}

**Image URL:** {meal.get("strMealThumb", "")}
**YouTube:** {meal.get("strYoutube", "")}
"""

    except requests.RequestException as e:
        return f"API error: {str(e)}"


@tool
def search_recipes_by_category(category: str) -> str:
    """
    Search recipes by category (e.g., Chicken, Seafood, Vegetarian, Dessert).
    Returns a formatted list of meals in that category.
    """
    try:
        url = f"{MEALDB_BASE_URL}/filter.php"
        response = requests.get(url, params={"c": category}, timeout=10)
        response.raise_for_status()
        data = response.json()

        meals = data.get("meals")
        if not meals:
            return f"No recipes found for category '{category}'."

        meal_lines = []
        for m in meals[:6]:
            title = m.get("strMeal", "")
            image_url = m.get("strMealThumb", "")
            meal_lines.append(f"- **{title}**\n  Image: {image_url}")

        meals_text = "\n\n".join(meal_lines)

        return f"""## 📂 Recipes in Category: {category}

Here are some meals you can try:

{meals_text}
"""

    except requests.RequestException as e:
        return f"API error: {str(e)}"