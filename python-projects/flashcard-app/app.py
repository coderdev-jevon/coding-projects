from datetime import date, timedelta
from flask import Flask, render_template, request, redirect, url_for, Response
import json
import os
from pathlib import Path
import random

# Path to the json database
DATA_PATH = Path("cards.json")

app = Flask(__name__)
def write_database(data: dict) -> bool:
    try:
        with DATA_PATH.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            return True
    except (FileNotFoundError, PermissionError, OSError):
        return False
# Return empty dict if Error
def read_database() -> dict:
    try:
        with DATA_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError, OSError):
        return {}

# Function to read all cards inside a deck
def read_deck(deck_name: str) -> list:
    data = read_database()

    if deck_name not in data:
        return False, []

    return True, data[deck_name]
# function to save added new deck, return True if successful, return False if failed
def save_new_deck(deck_name: str) -> bool:
    deck_name = deck_name.strip()
    if not deck_name:
        return False
    try: 
        if not DATA_PATH.exists():
            # If file doesn't exist, add empty dict to the json database
            empty = {}
            with DATA_PATH.open("w", encoding="utf-8") as f:
                json.dump(empty, f, ensure_ascii=False, indent=2)

        # Add new dect to database
        with DATA_PATH.open("r+", encoding="utf-8") as f:
            data = json.load(f)
            # Prevent overwriting same deck name
            if deck_name in data:
                return False
            data[deck_name] = []
            # Reset file pointer
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=2)
            # Clear leftover old content
            f.truncate()
        return True
            
    except (PermissionError, json.JSONDecodeError, FileNotFoundError, OSError):
        return False

def get_id(deck_name: str, data: dict) -> int:
    if deck_name not in data:
        return 0

    cards = data[deck_name]
    max_id = 0
    for card in cards:
        if max_id < card["id"]:
            max_id = card["id"]
    return max_id + 1

def parse_time(time_str: str):
    return date.strptime(time_str, "%Y-%m-%d")

@app.route("/")
def home():
    data = read_database()
    deck_names = data.keys()
    return render_template("home.html", deck_names=deck_names)

@app.route("/add-deck", methods=["GET", "POST"])
def add_deck():
    if request.method == "POST":
        name = request.form.get("name")
        # Get the bool info whether saving the new deck successful or not
        is_success = save_new_deck(name)
        if not is_success:
            return Response("New deck failed to add", 403)
        return redirect(url_for("home"))
    return render_template("add-deck.html")

@app.route("/delete-deck", methods=["POST"])
def delete_deck():
    name = request.form.get("name")
    data = read_database()

    if name not in data:
        return Response("Deletion failed", 403)
    
    del data[name]
    # Overwrite the old data
    is_success = write_database(data)
    if not is_success:
        return Response("Deletion failed", 500)
    
    return redirect(url_for("home"))

@app.route("/<deck_name>")
def view_deck(deck_name):
    success, cards = read_deck(deck_name)
    # Return value from read_deck func is (bool, list), get cards[0] to see successful or not
    if not success:
        return Response("Deck name not found", 404)
    
    return render_template("deck.html", cards=cards[:5], deck_name=deck_name)

@app.route("/<deck_name>/all-cards")
def view_all_cards(deck_name):
    success, cards = read_deck(deck_name)
    if not success:
        return Response("Deck name not found", 404)

    return render_template("deck-whole.html", cards=cards, deck_name=deck_name)

@app.route("/<deck_name>/add-card", methods=["GET", "POST"])
def add_card(deck_name):
    if request.method == "POST":
        data = read_database()
        if deck_name not in data:
            return Response("Deck not found", 404)
        deck = data[deck_name]

        front = request.form.get("front").strip()
        back = request.form.get("back").strip()

        if not front or not back:
            return Response("Input is not valid", 400)

        # Create temporary dict to store each card data
        now_str = date.today().strftime("%Y-%m-%d")
        new_id = get_id(deck_name, data)

        if new_id == 0:
            return Response("ID Failed to generate", 500)
        tmp = {
            "id": new_id,
            "date_created": now_str,
            "front": front,
            "back": back,
            "mastered": False,
            "last_reviewed": None # add last reviewed to not repeat a card in a day
        }

        deck.append(tmp)

        # Write the new update to database
        try:
            with DATA_PATH.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            return Response("Add Card Failed", 500)
        
        return redirect(url_for("view_deck", deck_name=deck_name))

    # GET
    return render_template("add-card.html", deck_name=deck_name)

@app.route("/delete-card", methods=["POST"])
def delete_card():
    id_str = request.form.get("id")
    id = int(id_str)
    deck_name = request.form.get("deck_name")
    data = read_database()

    if deck_name not in data:
        return Response("Deck not found", 403)

    # Remove card
    for card in data[deck_name]:
        if card["id"] == id:
            data[deck_name].remove(card)
    
    # Update database
    is_success = write_database(data)
    if not is_success:
        return Response("Deletion failed", 500)

    return redirect(url_for("view_deck", deck_name=deck_name))

@app.route("/<deck_name>/review", methods=["GET", "POST"])
def review_deck(deck_name):
    success, cards = read_deck(deck_name)

    if not success:
        return Response("Deck name not found", 404)

    if not cards:
        return Response("Deck is empty", 404)

    # Filter only not mastered cards and if last reviewed time is not 1 day less than today
    today = date.today()
    one_day = timedelta(days=1)
    not_mastered = []
    for card in cards:
        # Skip mastered cards
        if card["mastered"] == True:
            continue

        last_reviewed = card["last_reviewed"]
        if last_reviewed is None:
            not_mastered.append(card)
        else:
            last_reviewed = parse_time(last_reviewed)
            if today - last_reviewed >= one_day:
                not_mastered.append(card)

    if request.method == "POST":
        id = int(request.form.get("id"))
        action = request.form.get("action")
        data = read_database()
        current_card = None

        # Read the database to find the card targeted, because card data in not_mastered is removed
        data = read_database()
        if deck_name not in data:
            return Response("Deck not found", 404)
        deck = data[deck_name]

        # Specifying the card opened before to reveal it if action == "reveal"
        for card in deck:
            if card["id"] == id:
                current_card = card

        if current_card is None:
            return Response("Card Error", 404)
        
        # Reveal card
        if action == "reveal":
            return render_template("review.html", card=current_card, deck_name=deck_name, is_revealed=True)
        # Change card mastered boolean if easy and proceed to the next card
        elif action == "easy":
            for card in deck:
                if card["id"] == id:
                    # Change mastered status to True and delete last_reviewed data, 
                    # to make it convenient if user wants to change the mastered status back
                    card["mastered"] = True
                    card["last_reviewed"] = None

            # Update database
            is_success = write_database(data)
            if not is_success:
                return Response("Update failed", 500)

            return redirect(url_for("review_deck", deck_name=deck_name))
        # Proceed to the next card when user click hard
        elif action == "hard":
            for card in deck:
                if card["id"] == id:
                    today_str = date.today().strftime("%Y-%m-%d")
                    card["last_reviewed"] = today_str

            # Update database
            is_success = write_database(data)
            if not is_success:
                return Response("Update failed", 500)
            
            return redirect(url_for("review_deck", deck_name=deck_name))

    if not not_mastered:
        return render_template("review-complete.html", deck_name=deck_name)
    
    # Choose random card
    current_card = random.choice(not_mastered)
    is_revealed = False
    
    return render_template("review.html", card=current_card, deck_name=deck_name, is_revealed=is_revealed)

# Route to change mastered status
@app.route("/change-status", methods=["POST"])
def change_status():
    id = int(request.form.get("id"))
    deck_name = request.form.get("deck_name")

    data = read_database()
    deck = data[deck_name]

    for card in deck:
        if card["id"] == id:
            # Flip mastered status
            card["mastered"] = not card["mastered"]

    success = write_database(data)
    if not success:
        return Response("Update failed", 500)
    
    return redirect(url_for("view_all_cards", deck_name=deck_name))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)