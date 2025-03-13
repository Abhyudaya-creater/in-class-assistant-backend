from flask import Flask, request, jsonify
from appwrite.client import Client
from appwrite.services.databases import Databases
from twilio.rest import Client as TwilioClient
import random
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

# Appwrite Connection
client = Client()
client.set_endpoint("https://cloud.appwrite.io/v1")
client.set_project("67d1bef80033c718faf7")
client.set_key("In-Class-Assistant")
database = Databases(client)

# Twilio OTP Setup


#twilio_client = TwilioClient(os.getenv("AC4fd3f2a0f4c670b06f9515e58169b095"), os.getenv("712d02581a9b6d7493e6a07c50e3c830"))
twilio_client = TwilioClient("YOUR_TWILIO_SID", "YOUR_TWILIO_AUTH_TOKEN")

TWILIO_PHONE = "+917350672910"

# Verify Email & OTP
@app.route("/verify-email", methods=["POST"])
def verify_email():
    data = request.json
    email = data.get("email")
    
    user = database.list_documents("67d1c28200245cdac7de", "67d1c7ab0037775c5d03", query=["equal('email', email)"])
    if not user["documents"]:
        return jsonify({"error": "Unauthorized Email"}), 403
    
    otp = random.randint(100000, 999999)
    database.update_document("67d1c28200245cdac7de", "67d1c7ab0037775c5d03", user["documents"][0]["$id"], {"otp": otp})
    twilio_client.messages.create(to=email, from_=TWILIO_PHONE, body=f"Your OTP: {otp}")
    return jsonify({"message": "OTP Sent"})

if __name__ == "__main__":
    app.run(debug=True)