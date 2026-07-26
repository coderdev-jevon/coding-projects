# Directing file path
FILENAME = Path("expense.json")

from collections import defaultdict, Counter
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from pathlib import Path

app = Flask(__name__)

# Reading main json data
def load_data():
    if not FILENAME.exists():
        return []
    try:
        with FILENAME.open('r', encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # File exists but content is broken / empty
        return []

# Overwriting main json data
def save_data(updated_data):
    with FILENAME.open('w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=4)

@app.route("/")
def home():
    # Load data and sent it to html
    data_list = load_data()
    data_list = sorted(data_list, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)
    return render_template("home.html", datas=data_list)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")

    date = request.form.get('date')
    category = request.form.get('category')
    description = request.form.get('description')
    amount = request.form.get('amount')
    cost = request.form.get('cost')
    note = request.form.get('note', "").strip()

    if not date or not category or not description:
        return "Date/Category/Description cannot be empty", 400

    # Check the value of amount and cost
    try:
        amount = int(amount)
        cost = float(cost)
        if amount > 0 and cost > 0:
            ind_dict["amount"] = amount
            ind_dict["cost"] = cost
        else:
            return "Negative value is not accepted", 400
    except (ValueError, TypeError):
        return "Amount and Cost value is not valid", 400
    
    # Creating individual dictionary and store it to main data
    ind_dict = {}
    ind_dict["date"] = date
    ind_dict["category"] = category
    ind_dict["description"] = description

    ind_dict["total"] = ind_dict["amount"] * ind_dict["cost"]
    ind_dict["note"] = note

    # Reading main data and stores the data inside
    data_list = load_data()
    data_list.append(ind_dict) 
    save_data(data_list)

    return redirect(url_for("home"))

@app.route("/summary")
def summary():
    data_list = load_data()
    # Get the date and time today, and take the month value
    now = datetime.now()
    now_month = now.month
    now_year = now.year

    # Track this month's expense
    this_month_expense = sum([x["total"] for x in data_list if (dt :=datetime.strptime(x["date"], "%Y-%m-%d")).month == now_month and dt.year == now_year])

    per_category_expense = defaultdict(float)

    # Group data based on categories
    for data in data_list:
        per_category_expense[data["category"]] += data["total"]

    # Counter for each categories total spendings
    count = Counter([data["category"] for data in data_list])

    return render_template("summary.html", per_category_expense=per_category_expense, this_month_expense=this_month_expense, count=count)

@app.route("/api")
def api():
    data_list = load_data()
    return jsonify(data_list)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)