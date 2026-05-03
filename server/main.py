from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from numpy import exp
from pydantic import BaseModel
import storage
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
# Initialize Gemini client with API key from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  


#create gemini model instance
model = genai.GenerativeModel("gemini-1.5-flash")





#creating fastapi app instance

app = FastAPI(title="Expense Tracker API")

#allowing CORS for all origins (for development purposes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (fine for local dev)
    allow_methods=["*"],
    allow_headers=["*"],
)
# Pydantic model — defines what data shape we EXPECT when adding an expense
# FastAPI automatically validates this for us

class ExpensesInput(BaseModel):  #defines the expected shape of the input data when adding a new expense

    amount: float
    category: str
    description: str

# ENDPOINTS


# GET /expenses → returns all expenses
@app.get("/expenses")
def get_expenses():
    return storage.load_expenses()

# POST /expenses → adds a new expense
# The request body must match ExpenseInput shape
@app.post("/expenses")
def add_expense(expense: ExpensesInput):
    new = storage.add_expense(
        amount=expense.amount,
        category=expense.category,
        description=expense.description
    )
    return new  # return the newly created expense


# DELETE /expenses/{id} → deletes expense by ID
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id:int):
    deleted =storage.delete_expense(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Deleted successfully"} #return a success message if the expense was deleted


#GET /summery → returns a summary of expenses by category
@app.get("/summery")
def get_summary():
    expenses = storage.load_expenses()
    summary = {}
    for expense in expenses:
        cat = expense["category"]
        # If category not seen yet, start at 0
        if cat not in summary:
            summary[cat] = 0
        summary[cat] += expense["amount"]
    return summary
    

# GET /health → simple check to confirm API is running
@app.get("/health")
def health():
    return {"status": "ok"}


# NEW — AI ANALYSIS ENDPOINT

@app.get("/analyze")
def analyze_expenses():
    expenses =storage.load_expenses()

    if not expenses:
        raise HTTPException(status_code=400, detail="No expenses to analyze")           
    
    #build a summery of spending by category to send to gemini
    summary = {}
    total = 0
    for expense in expenses:
        cat=exp["category"]
        if cat not in summary:
            summary[cat] = 0
        summary[cat] += expense["amount"]
        total += exp["amount"]

    #format the data as readable text for ai
    summary_text= "Here is a summary of my expenses:\n"


# This is the prompt we send to Gemini
    # We give it our expense data and ask for specific advice
    prompt = f"""
    You are a helpful personal finance assistant.
    
    Here is a summary of my recent expenses (total: ${total:.2f}):
    {summary_text}
    
    Please do the following:
    1. Give a brief analysis of my spending pattern (2-3 sentences)
    2. Point out the top 2 areas where I'm spending the most
    3. Give 3 specific, practical tips to help me save money based on these categories
    4. Give my spending an overall score out of 10 and explain why
    
    Keep the response friendly, concise and actionable.
    """

     # Send the prompt to Gemini and get the response
    response = model.generate_content(prompt)

    # Return the AI's text response
    return {"analysis": response.text}