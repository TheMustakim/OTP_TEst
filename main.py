from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import random
from email.message import EmailMessage
from datetime import datetime

app = Flask(__name__)
CORS(app)  # So Netlify can talk to it

# --- Email Configuration ---
SENDER_EMAIL = "mustakim.api@zohomail.com"
SENDER_PASS = "XunJ56HJYkC6"  # ⚠️ Keep this safe
SMTP_SERVER = "smtp.zoho.com"
SMTP_PORT = 465

# --- OTP Email Function ---
def send_otp_email(receiver_email):
    otp = random.randint(100000, 999999)

    msg = EmailMessage()
    msg["Subject"] = "Your One-Time Passcode 🌟"
    msg["From"] = f"SecureAuth <{SENDER_EMAIL}>"
    msg["To"] = receiver_email

    msg.set_content(f"Your OTP is: {otp}")

    html = f"""
    <html><body>
        <div style="font-family:Arial;text-align:center;padding:20px;">
            <h2>🔐 Your Secure Access Code</h2>
            <p>Use this one-time code:</p>
            <div style="font-size:32px;font-weight:bold;margin:20px;">{otp}</div>
            <p>Expires in 5 minutes.</p>
        </div>
    </body></html>
    """
    msg.add_alternative(html, subtype="html")

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASS)
            server.send_message(msg)
        return otp
    except Exception as e:
        print(f"❌ Email error: {e}")
        return None

# --- Route to Handle Frontend Request ---
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    otp = send_otp_email(email)

    if otp:
        print(f"✅ OTP sent to {email} for {name}")
        return jsonify({"success": True, "message": f"OTP sent to {email}!"})
    else:
        return jsonify({"success": False, "message": "Failed to send OTP"}), 500

# --- Main ---
if __name__ == "__main__":
    app.run()
