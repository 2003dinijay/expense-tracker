# 💰 AI-Powered Expense Tracker

A full-stack expense tracking application built with **FastAPI**, **Streamlit**, and **Google Gemini AI**. Log your expenses, visualize spending patterns with charts, and get personalized AI-powered financial insights.

---

## 🚀 Features

- ➕ Add and delete expenses with categories
- 📋 Filter expenses by category
- 📊 Interactive pie and bar charts (Plotly)
- 🤖 AI spending analysis with score and tips (Gemini)
- 💬 Chat with AI about your finances
- 📈 Summary metrics (total, count, average)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI + Uvicorn |
| Frontend UI | Streamlit |
| AI | Google Gemini 1.5 Flash |
| Charts | Plotly Express |
| Data | JSON file (local storage) |
| Environment | python-dotenv |

---

## 📁 Project Structure

```
expense-tracker/
├── backend/
│   ├── main.py          # FastAPI app & all endpoints
│   └── storage.py       # JSON file read/write logic
├── frontend/
│   └── app.py           # Streamlit UI
├── .env                 # API keys (never committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/2003dinijay/expense-tracker.git
cd expense-tracker
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows (Git Bash)
source venv/Scripts/activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root folder:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your free Gemini API key at [aistudio.google.com](https://aistudio.google.com).

---

## ▶️ Running the App

You need **two terminals** open at the same time.

**Terminal 1 — Start the backend:**

```bash
cd backend
uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

**Terminal 2 — Start the frontend:**

```bash
cd frontend
streamlit run app.py
```

Frontend runs at: `http://localhost:8501`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/expenses` | Get all expenses (optional `?category=Food`) |
| `POST` | `/expenses` | Add a new expense |
| `DELETE` | `/expenses/{id}` | Delete an expense by ID |
| `GET` | `/summary` | Get totals grouped by category |
| `GET` | `/analyze` | Get AI analysis of spending |
| `POST` | `/chat` | Chat with AI about your finances |
| `GET` | `/health` | Health check |

---

## 📸 App Preview

| Tab | What you'll see |
|---|---|
| 📋 Expenses | List of all expenses with delete option and summary metrics |
| 📊 Charts | Pie chart and bar chart of spending by category |
| 🤖 AI | Spending score, tips, and a live chat with Gemini |

---

## 🧠 What I Learned Building This

- Building REST APIs with **FastAPI** (routes, Pydantic validation, query params, error handling)
- Creating UIs in pure Python with **Streamlit** (widgets, layouts, tabs, session state)
- How **frontend and backend communicate** via HTTP requests
- **Prompt engineering** with the Gemini API to get structured JSON responses
- Managing environment variables and project structure

---

## 📦 Requirements

```
fastapi
uvicorn
streamlit
requests
plotly
pandas
google-generativeai
python-dotenv
```

Install all with:

```bash
pip install -r requirements.txt
```

---

## 📝 License

MIT License-free to use and modify.
