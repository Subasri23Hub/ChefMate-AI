# 👨‍🍳 ChefMate AI

> **Your AI-powered Food Intelligence Assistant**
> *"AI has no age limit. It can assist anyone, anywhere, in everyday life."*

---

## 🎯 Overview

ChefMate AI is a production-grade, multi-agent AI application built with **LangGraph** and **Gemini 2.5 Flash**. It combines four specialized AI agents to help users with every aspect of food — from finding recipes to planning meals, getting nutrition advice, and substituting ingredients.

---

## 🧠 Architecture

```
User Query
    │
    ▼
Router Agent (LangGraph)
    │
    ├── 🍽️ Recipe Agent       → TheMealDB API + Gemini
    ├── 🗓️ Meal Planner Agent → Gemini Reasoning
    ├── 🥗 Nutrition Advisor  → Prebuilt Agent + Tools
    └── 🔄 Substitute Agent  → Prebuilt Agent + Tools
```

### Agents

| Agent | Type | Purpose |
|-------|------|---------|
| **Recipe Agent** | Custom LangGraph `StateGraph` | Fetches recipes from TheMealDB API |
| **Meal Planner Agent** | Custom LangGraph `StateGraph` | Generates structured meal plans |
| **Nutrition Advisor** | Prebuilt LangChain Agent | Personalized food & health advice |
| **Ingredient Substitute** | Prebuilt LangChain Agent | Smart ingredient alternatives |
| **Router Agent** | LangGraph `StateGraph` | Auto-classifies and routes queries |

---

## ⚙️ Tech Stack

- **Python 3.10+**
- **Streamlit** — Modern chat UI
- **LangGraph** — Multi-agent orchestration
- **LangChain** — Agent framework & tools
- **Gemini 2.5 Flash** — via `ChatGoogleGenerativeAI`
- **TheMealDB API** — Free recipe database (no key required)
- **python-dotenv** — Environment management

---

## 🚀 Quick Start

### 1. Clone & Navigate

```bash
cd chefmate-ai
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Edit the `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Get your free Gemini API key at: https://aistudio.google.com/

### 5. Run the App

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 💬 Example Queries

| Query | Routed To |
|-------|-----------|
| "Give me a biryani recipe" | 🍽️ Recipe Agent |
| "How to make chocolate cake?" | 🍽️ Recipe Agent |
| "Create a 7-day meal plan" | 🗓️ Meal Planner |
| "What should I eat for weight loss?" | 🥗 Nutrition Advisor |
| "I don't have butter, what can I use?" | 🔄 Substitute Agent |
| "Suggest a healthy breakfast" | 🥗 Nutrition Advisor |
| "Vegan substitute for eggs?" | 🔄 Substitute Agent |

---

## 📁 Project Structure

```
chefmate-ai/
│
├── app.py                      # Main Streamlit application
├── .env                        # API keys (not committed)
├── .gitignore
├── requirements.txt
├── README.md
│
├── config/
│   ├── __init__.py
│   └── settings.py             # LLM configuration
│
├── agents/
│   ├── __init__.py
│   ├── recipe_graph.py         # Custom LangGraph recipe agent
│   ├── meal_planner_graph.py   # Custom LangGraph planner agent
│   ├── nutrition_agent.py      # Prebuilt nutrition advisor
│   ├── substitute_agent.py     # Prebuilt substitute advisor
│   └── router_graph.py         # Query router
│
├── tools/
│   ├── __init__.py
│   ├── recipe_tools.py         # TheMealDB API tools
│   ├── nutrition_tools.py      # Nutrition advice tools
│   ├── substitute_tools.py     # Ingredient substitute tools
│   └── formatter.py            # Output formatting helpers
│
├── ui/
│   ├── __init__.py
│   └── components.py           # Reusable Streamlit components
│
└── assets/
    └── (logo and static files)
```

---

## 🔑 API Keys

| Service | Required | Get Key |
|---------|----------|---------|
| Google Gemini | ✅ Yes | [aistudio.google.com](https://aistudio.google.com/) |
| TheMealDB | ❌ No | Free, no signup |

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

<div align="center">
Built with ❤️ using LangGraph + Gemini 2.5 Flash
</div>
