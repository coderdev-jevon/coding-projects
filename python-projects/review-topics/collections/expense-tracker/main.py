from collections import defaultdict, Counter
from config import FILENAME, HOST, PORT
from database import load_data, save_data
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import calculate_total, filter_expenses_in_date_range, get_latest_expenses
import os
from utils import parse_date

app = Flask(__name__)

@app.route("/")
def home():
    # Load data and sent it to html
    expenses = get_latest_expenses(load_data(), 10)
    return render_template("home.html", datas=expenses)

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

    # Individual dict before append to the main json data
    ind_dict = {}
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
    ind_dict["date"] = date
    ind_dict["category"] = category
    ind_dict["description"] = description

    ind_dict["total"] = calculate_total(amount, cost)
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
    this_month_expense = sum([x["total"] for x in data_list if (dt := parse_date(x["date"])).month == now_month and dt.year == now_year])

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

# Filter expenses in the last 7 days
@app.route("/lastsevendays")
def last_seven_days():
    # Use function from utils to filter the last seven days expense
    last_seven_days_expenses = filter_expenses_in_date_range(load_data(), 7)

    return render_template("lastsevendays.html", datas=last_seven_days_expenses)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", PORT))
    app.run(debug=True, host=HOST, port=port)