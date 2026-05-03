import json
import os
from datetime import datetime

#This file handles reading/writing expenses to a JSON file on disk. It provides functions to load all expenses, save a list of expenses, add a new expense, and delete an expense by ID.


DATA_FILE ="expenses.json"


def load_expenses():
       # If the file doesn't exist yet, return an empty list
    if not os.path.exists(DATA_FILE):
        return []
         # Open the file and parse the JSON into a Python list
    with open(DATA_FILE,"r") as f:
        return json.load(f)

def save_expenses(expenses):
     # Take a Python list and write it to the JSON file
    with open(DATA_FILE,"w") as f:
        # Save expenses to the JSON file
        json.dump(expenses,f,indent=2)

def add_expense(amount:float, category:str, description:str):
    # Load existing expenses
    expenses = load_expenses()
    # Create a new expense as a dictionary
    new_expense = {
        "id": len(expenses) + 1,          # simple auto-increment ID
        "amount": amount,
        "category": category,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d")  # today's date
    }
    # Add the new expense to the list
    
    expenses.append(new_expense)
    save_expenses(expenses)
    return new_expense

def delete_expense(expense_id: int):
    expenses = load_expenses()
    # Keep all expenses EXCEPT the one with the matching ID
    updated = [e for e in expenses if e["id"] != expense_id]
    save_expenses(updated)
    return len(expenses) != len(updated)  # returns True if something was deleted