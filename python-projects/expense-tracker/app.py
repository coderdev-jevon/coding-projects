from datetime import date
from flask import Flask, render_template, request, Response, redirect, url_for
import os
import pandas as pd

FILE_PATH = "expenses.csv"
EXPENSE_CATEGORIES = ["Food", "Transport", "Utility", "Shopping", "Health", "Entertainment", "Education", "Others"]
PAYMENT_METHODS = ["Cash", "Debit Card", "Credit Card", "E-wallet", "Others"]

app = Flask(__name__)

def read_expense_df():
    try:
        return pd.read_csv(FILE_PATH)
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, pd.errors.ParserError):
        return pd.DataFrame(columns=["date", "category", "description", "amount", "payment"])
def init_csv():
    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=["date", "category", "description", "amount", "payment"])
        df.to_csv(FILE_PATH, index=False)
@app.route("/", methods=["GET", "POST"])
def index():
    init_csv()
    if request.method == "POST":
        # Read csv file
        try:
            df = pd.read_csv(FILE_PATH)
        except (FileNotFoundError, PermissionError, UnicodeDecodeError, pd.errors.ParserError):
            return Response("Failed to read file", 403)

        date = request.form.get("date")
        category = request.form.get("category")
        description = request.form.get("description").strip()
        amount = request.form.get("amount").strip()
        payment = request.form.get("payment")

        if not description or not amount:
            return Response("Invalid description or amount", 403)

        try:
            amount = float(amount)
        except ValueError:
            return Response("Amount input is not a valid number", 403)
        
        # Create temporary dict and append it to pandas database
        tmp = {
            "date": date,
            "category": category,
            "description": description,
            "amount": amount,
            "payment": payment
        }

        # Add to the last index of the database
        df.loc[len(df)] = tmp

        # Overwrite old csv data after sorting, before sorting change date column to datetime
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date", ascending=False)
        df.to_csv(FILE_PATH, index=False)
        return redirect(url_for("index"))

    try:
        df = pd.read_csv(FILE_PATH)
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, pd.errors.ParserError):
        return Response("Failed to read file", 403)

    mean = df["amount"].mean().round(2)
    total = df["amount"].sum().round(2)
    # Send it to HTML
    rows = df.itertuples()
    return render_template("index.html", rows=rows, mean=mean, total=total)

@app.route("/delete", methods=["POST"])
def delete():
    try:
        # Get index sent by hidden input
        index = int(request.form.get("index"))
        # Read csv file, drop it, and reset index
        df = pd.read_csv(FILE_PATH)
        df = df.drop(index=index)
        df = df.reset_index(drop=True)
        # Send back to csv
        df.to_csv(FILE_PATH, index=False)
    except Exception as e:
        return Response(f"Delete failed: {e}", 403)

    return redirect(url_for("index"))
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)