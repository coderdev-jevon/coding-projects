from pathlib import Path

# Path for the logs folder
folder = Path('transaction-logs')

INCOME_CATEGORIES = [
    "Salary",
    "Bonus",
    "Freelance",
    "Dividend",
    "Allowance",
    "Rent Income",
    "Commission"
]

EXPENSE_CATEGORIES = [
    "Food",
    "Transport",
    "Utility",
    "Shopping",
    "Entertainment",
    "Healthcare",
    "Education"
]

SAMPLE_DESCRIPTIONS = {
    # Income
    "Salary": ["Monthly salary", "Basic wage", "Monthly pay"],
    "Bonus": ["Performance bonus", "Year-end bonus", "Quarterly reward"],
    "Freelance": ["Project payment", "Client service fee", "Freelance job income"],
    "Dividend": ["Stock dividend", "Investment dividend", "Fund profit distribution"],
    "Allowance": ["Family allowance", "Living allowance", "Daily stipend"],
    "Rent Income": ["Apartment rent", "Property rental income"],
    "Commission": ["Sales commission", "Referral commission"],

    # Expense
    "Food": ["Lunch", "Dinner", "Snack", "Groceries", "Cafe drink"],
    "Transport": ["Fuel", "Taxi fare", "Bus ticket", "Motorcycle maintenance"],
    "Utility": ["Electric bill", "Internet bill", "Water bill"],
    "Shopping": ["Clothes purchase", "Daily necessities", "Electronic accessory"],
    "Entertainment": ["Movie ticket", "Game purchase", "Concert ticket"],
    "Healthcare": ["Medicine", "Medical check-up", "Clinic consultation fee"],
    "Education": ["Textbook", "Online course fee", "Training material"]
}