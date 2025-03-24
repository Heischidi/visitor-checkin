# 🚀 Visitor Check-in System

## 📌 Project Overview
This is a **web-based visitor check-in system** that allows visitors to check in using a **QR code**, while admins can **approve or reject** visitor requests in real-time.

---

## ✅ Features
- **Visitor Check-in Form** – Visitors fill out a form when checking in.
- **QR Code Generation** – Each visitor gets a unique QR code.
- **Admin Dashboard** – Admins can view, approve, or reject check-ins.
- **Real-time Updates** – Visitor status updates instantly.
- **Firebase Integration** – Stores visitor records securely.
- **Flask APIs** – Separate APIs for visitors and admins.

---

## 🛠 Installation & Setup
### **1️⃣ Install Required Packages**
Ensure Python and pip are installed, then run:
```bash
pip install -r requirements.txt
```

### **2️⃣ Start the Visitor API**
```bash
python visitor_api.py
```
This runs the **visitor check-in system** on:
```
http://127.0.0.1:5000
```

### **3️⃣ Start the Admin API**
```bash
python admin_api.py
```
This runs the **admin dashboard** on:
```
http://127.0.0.1:5001
```

### **4️⃣ Open in Browser**
- **Visitor Check-in Form:** `visitor check in form.html`
- **Admin Dashboard:** `admin.html`

---

## 🔗 API Endpoints
### **Visitor API (`visitor_api.py` on port `5000`)**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/checkin` | Visitor submits check-in form |
| `POST` | `/generate_qr` | Generates a QR code for check-in |

### **Admin API (`admin_api.py` on port `5001`)**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/visitors` | Fetch all visitor records |
| `POST` | `/approve/<visitor_id>` | Approves a visitor |
| `POST` | `/reject/<visitor_id>` | Rejects a visitor |

---

## ⚠️ Important Notes
- Ensure `serviceAccountKey.json` is configured for Firebase.
- Run **both APIs** simultaneously for full functionality.
- Make sure the visitor API is running **before generating QR codes**.

---

## 📝 Author & Credits
**Developed by:** _Chidi_  
For inquiries, contact: _your_email@example.com_

---
