from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template
import time


# Initialize Firebase
cred = credentials.Certificate("tamagotchidoughmomo-5828e-firebase-adminsdk-fbsvc-c566d745ca.json")  # Your Firebase key JSON
firebase_admin.initialize_app(cred)
db = firestore.client()

# Flask app setup
tamagotchi = Flask(__name__)

def decay_pet_stats():
    pet_ref = db.collection("pets").document("Kitty")
    pet_data = pet_ref.get().to_dict()

    # Get last update time (default to now if missing)
    last_updated = pet_data.get("last_updated", time.time())

    # Time passed in minutes
    minutes_passed = (time.time() - last_updated) / 60

    if minutes_passed >= 5:  # Only update every 5 minutes
        new_hunger = min(100, pet_data["hunger"] + int(minutes_passed))  # Hunger increases
        new_happiness = max(0, pet_data["happiness"] - int(minutes_passed))  # Happiness decreases

        # Update Firestore with new values and the current timestamp
        pet_ref.update({
            "hunger": new_hunger,
            "happiness": new_happiness,
            "last_updated": time.time()
        })

# Fetch pet data
@tamagotchi.route("/pet", methods=["GET"])
def get_pet():
    decay_pet_stats()  # Ensure values update before sending
    pet_ref = db.collection("pets").document("Kitty")
    pet_data = pet_ref.get().to_dict()
    return jsonify(pet_data)

# Feed the pet (reduces hunger)
@tamagotchi.route("/feed", methods=["POST"])
def feed_pet():
    pet_ref = db.collection("pets").document("LilBuddy")
    pet_data = pet_ref.get().to_dict()

    new_hunger = max(0, pet_data["hunger"] - 10)  # Feeding reduces hunger
    pet_ref.update({"hunger": new_hunger})

    return jsonify({"message": "Fed the pet!", "hunger": new_hunger})

# Play with the pet (increases happiness)
@tamagotchi.route("/play", methods=["POST"])
def play_with_pet():
    pet_ref = db.collection("pets").document("LilBuddy")
    pet_data = pet_ref.get().to_dict()

    new_happiness = min(100, pet_data["happiness"] + 10)  # Playing increases happiness
    pet_ref.update({"happiness": new_happiness})

    return jsonify({"message": "Played with the pet!", "happiness": new_happiness})

@tamagotchi.route("/")
def home():
    return render_template("index.html")

# Run the Flask app
if __name__ == "__main__":
    tamagotchi.run(host="0.0.0.0", port=10000)  # Render uses dynamic ports
