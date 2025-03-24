from google.cloud import firestore
import os

# Ensure the credentials are set
print("Checking credentials...")
if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
    print("ERROR: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
    exit(1)

print("Environment variable is set to:", os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

try:
    # Initialize Firestore client
    print("Initializing Firestore client...")
    db = firestore.Client()

    # Test Firestore connection
    print("Testing Firestore connection...")
    doc_ref = db.collection("test").document("debug_test")
    doc_ref.set({"status": "connected", "timestamp": firestore.SERVER_TIMESTAMP})
    print("Firestore connection successful! Test document written.")
except Exception as e:
    print("Error connecting to Firestore:", str(e))
