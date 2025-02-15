import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase credentials
cred = credentials.Certificate("tamagotchidoughmomo-5828e-firebase-adminsdk-fbsvc-c566d745ca.json")  # Use your actual file name
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# Example: Create or update pet data
pet_ref = db.collection("pets").document("Cat")
pet_ref.set({"hunger": 50, "happiness": 70})

print("Pet data updated!")

# Fetch pet data
pet_data = pet_ref.get().to_dict()
print(f"Pet Hunger: {pet_data['hunger']}")

# Update hunger level
pet_ref.update({"hunger": pet_data["hunger"] - 10})
print("Fed the pet! Hunger decreased.")