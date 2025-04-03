import firebase_admin
from firebase_admin import credentials, firestore

# Path to your Firebase private key JSON file (Update path accordingly)
cred = credentials.Certificate(r"C:\Users\kunal poojary\OneDrive\Desktop\MarketMood\Backend\marketmood.json")

# Initialize Firebase App
firebase_admin.initialize_app(cred)

# Get Firestore Database
db = firestore.client()
