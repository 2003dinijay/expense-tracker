from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import storage

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