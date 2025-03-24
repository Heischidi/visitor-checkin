import json
from flask import Flask, request, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")

# Load Firebase credentials from environment variable
firebase_credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if not firebase_credentials_json:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable is not set.")
cred = credentials.Certificate(json.loads(firebase_credentials_json))
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/admin")
def admin_dashboard():
    """Render the admin dashboard with visitor data."""
    checkins_ref = db.collection("checkins").stream()
    visitor_list = [{"id": doc.id, **doc.to_dict()} for doc in checkins_ref]
    return render_template("admin.html", visitors=visitor_list)

@app.route("/approve/<visitor_id>", methods=["POST"])
def approve_visitor(visitor_id):
    """Approve a visitor."""
    try:
        visitor_ref = db.collection("checkins").document(visitor_id)
        visitor_ref.update({"status": "approved"})
        return jsonify({"message": "Visitor approved."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/reject/<visitor_id>", methods=["POST"])
def reject_visitor(visitor_id):
    """Reject a visitor."""
    try:
        visitor_ref = db.collection("checkins").document(visitor_id)
        visitor_ref.update({"status": "rejected"})
        return jsonify({"message": "Visitor rejected."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    """Default home route."""
    return "Visitor Check-In System is Running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)
