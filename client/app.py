import streamlit as st
import requests
import plotly.express as px
import pandas as pd

API_URL = "http://localhost:8000"

# HELPER FUNCTIONS — talk to the FastAPI backend

def get_expenses():
    #send a GET request to the /expenses endpoint and return the list of expenses
    response = requests.get(f"{API_URL}/expenses")
    return response.json() #convert json response to python list


def add_expense(amount, category, description):
    #send a POST request to the /expenses endpoint with the new expense data
    res = requests.post(f"{API_URL}/expenses", json={
        "amount": amount,
        "category": category,
        "description": description
    })
    return res.json()

def delete_expense(expense_id):
    #send DELETE request to the /expenses/{id} endpoint to delete the specified expense
    res = requests.delete(f"{API_URL}/expenses/{expense_id}")
    return res.json() #returns dict like {"message": "Deleted successfully"} if deletion was successful, or an error message if not


def get_summary():
    #send a GET request to the /summery endpoint to get the summary of expenses by category
    res = requests.get(f"{API_URL}/summery")
    return res.json() #returns a dict like {"Food": 150.0, "Transport": 75.0, ...}  

#PAGE CONFIG


st.set_page_config(page_title="💰Expense Tracker", page_icon="💸")
st.title("💰 AI-Powered Expense Tracker")

#SIDEBAR — add new expense

st.sidebar.header("➕ Add New Expense")

#These are the input fields for adding a new expense. The user can enter the amount, category, and description of the expense.  

amount = st.sidebar.number_input("Amount ($)", min_value=0.01, step=0.01)
category = st.sidebar.selectbox("Category", [
    "Food","Education", "Transport", "Entertainment",
    "Health", "Shopping", "Bills", "Other"
])
description = st.sidebar.text_input("Description")

if st.sidebar.button("Add Expense"):
    if description.strip() == "":
        st.sidebar.error("Please enter a description!")
    else:
        add_expense(amount, category, description)
        st.sidebar.success("Expense added! ✅")
        # Rerun the app so the new expense shows up immediately
        st.rerun()

# MAIN AREA — Split into 2 columns


col1, col2 = st.columns(2)

#LEFT COLUMN: Expense list 
with col1:
    st.subheader("📋 All Expenses")
    expenses = get_expenses()

    if not expenses:
        st.info("No expenses yet. Add one from the sidebar!")
    else:
        for exp in expenses:
            # Show each expense with a delete button next to it
            c1, c2 = st.columns([4, 1])
            with c1:
                st.write(f"**{exp['category']}** — LKR{exp['amount']:.2f} — {exp['description']} *(_{exp['date']}_)*")
            with c2:
                if st.button("🗑️", key=f"del_{exp['id']}"):
                    delete_expense(exp["id"])
                    st.rerun()

#RIGHT COLUMN: Charts
with col2:
    st.subheader("📊 Spending Summary")
    summary = get_summary()

    if not summary:
        st.info("No data to chart yet.")
    else:
        # Convert summary dict to a DataFrame for Plotly
        df = pd.DataFrame(list(summary.items()), columns=["Category", "Total"])

        # Pie chart
        pie = px.pie(df, names="Category", values="Total", title="Spending by Category")
        st.plotly_chart(pie, use_container_width=True)

        # Bar chart
        bar = px.bar(df, x="Category", y="Total", title="Amount per Category", color="Category")
        st.plotly_chart(bar, use_container_width=True)



st.divider()
st.subheader("🤖 AI Spending Analysis")

# Only show the button if there are expenses to analyze
expenses = get_expenses()
if not expenses:
    st.info("Add some expenses first, then come back here for AI analysis!")
else:
    if st.button("✨ Analyze My Spending with AI", type="primary"):
        # Show a spinner while waiting for the AI response
        with st.spinner("Gemini is analyzing your expenses..."):
            analysis, error = get_ai_analysis()

        if error:
            st.error(f"Error: {error}")
        else:
            # Display the AI response in a nice box
            st.success("Analysis complete!")
            st.markdown(analysis)