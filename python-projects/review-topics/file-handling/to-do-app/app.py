from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
import json
import os
from pathlib import Path

app = Flask(__name__)

DATA_FILE = Path("tasks.json")

# Read tasks data from JSON file
def load_tasks():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

# Overwrite data in JSON file
def save_tasks(tasks_list):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks_list, f, ensure_ascii=False, indent=4)

# Home Page
@app.route("/")
def home():
    tasks_list = load_tasks()
    return render_template("home.html", tasks=tasks_list)

# Add Page
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        # Get input from the user, strip it and create a dictionary for it
        task_name = request.form.get("name").strip()
        tasks_list = load_tasks()

        # If input is empty, return error message
        if not task_name:
            return "Task title cannot be empty", 400

        # If iinput is a duplicate, return error message
        for task in tasks_list:
            if task["title"] == task_name:
                return "Task title is a duplicate", 400
        
        task_dict = {}
        task_dict["title"] = task_name
        task_dict["completed"] = False

        tasks_list.append(task_dict)

        save_tasks(tasks_list)

        return redirect(url_for("home"))

# Delete
@app.route("/delete", methods=["POST"])
def delete():
    task_name = request.form.get("task_name")
    tasks_list = load_tasks()
    # List after deletion
    updated_tasks_list = []

    for task in tasks_list:
        if task["title"] != task_name:
            updated_tasks_list.append(task)

    save_tasks(updated_tasks_list)

    return redirect(url_for("home"))

# Change Completed Status
@app.route("/status", methods=["POST"])
def status():
    task_name = request.form.get("task_name")
    tasks_list = load_tasks()

    for task in tasks_list:
        if task["title"] == task_name:
            task["completed"] = not task["completed"]

    save_tasks(tasks_list)

    return redirect(url_for("home"))

# Edit Page
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        old_name = request.args.get("old_name")
        return render_template("edit.html", old_name=old_name)
    else:
        new_name = request.form.get("new_name")
        old_name = request.form.get("old_name").strp()
            
        tasks_list = load_tasks()

        for task in tasks_list:
            if task["title"] == old_name:
                task["title"] = new_name

        save_tasks(tasks_list)

        return redirect(url_for("home"))

# API Page
@app.route("/api")
def api():
    tasks_list = load_tasks()

    return jsonify(tasks_list)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
