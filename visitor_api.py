import json
import os
from flask import Flask, request, jsonify, render_template, make_response
from flask_cors import CORS # type: ignore
import qrcode
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore


# Check if the environment variable is set
cred_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if cred_json:
    try:
        json.loads(cred_json)
        print("✅ Environment variable is set correctly!")
    except json.JSONDecodeError as e:
        print(f"🚨 JSON Decode Error: {e}")
        raise ValueError("🚨 Invalid JSON format in GOOGLE_APPLICATION_CREDENTIALS_JSON.")
else:
    print("❌ GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable is not set.")
    raise ValueError("🚨 GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable is missing.")
# Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app, resources={r"/*": {"origins": "*"}})

# Ensure the QR code storage folder exists
QR_CODE_FOLDER = "static/qrcodes"
if not os.path.exists(QR_CODE_FOLDER):
    os.makedirs(QR_CODE_FOLDER)
print("✅ QR Code Folder Exists or Created!")

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

@app.route("/update_status", methods=["POST"])
def update_status():
    """Update visitor check-in status (approved/rejected)."""
    data = request.json
    visitor_id = data.get("visitor_id")
    status = data.get("status")

    if not visitor_id or status not in ["approved", "rejected"]:
        return jsonify({"error": "Invalid request"}), 400

    try:
        visitor_ref = db.collection("checkins").document(visitor_id)
        visitor_ref.update({"status": status})
        return jsonify({"message": f"Visitor {status} successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    """Default home route."""
    return "Visitor Check-In System is Running!"

@app.route("/checkin")
def checkin_form():
    """Render the visitor check-in form."""
    return render_template("checkin.html")

@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    """Generate a QR code linking to the check-in form."""
    form_url = "https://visitor-checkin.onrender.com/checkin"
    qr = qrcode.make(form_url)
    qr_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    qr_path = os.path.join(QR_CODE_FOLDER, qr_filename)
    qr.save(qr_path)

    print(f"✅ QR Code Generated: {qr_path}")

    return jsonify({
        "message": "QR code generated",
        "qr_code_url": f"https://visitor-checkin.onrender.com/static/qrcodes/{qr_filename}"
    })

@app.route("/submit_checkin", methods=["POST"])
def submit_checkin():
    """Process visitor check-in form submission."""
    data = request.json
    name = data.get("name")
    purpose = data.get("purpose")
    time_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not name or not purpose:
        response = make_response(jsonify({"error": "Missing required fields"}), 400)
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    checkin_data = {
        "name": name,
        "purpose": purpose,
        "time_in": time_in,
        "status": "pending"
    }

    try:
        db.collection("checkins").add(checkin_data)
        response = make_response(jsonify({
            "message": "Check-in submitted successfully",
            "status": "pending"
        }))
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    except Exception as e:
        response = make_response(jsonify({"error": str(e)}), 500)
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

@app.before_request
def handle_options_request():
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight"})
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
