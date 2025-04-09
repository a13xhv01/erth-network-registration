#!/usr/bin/env python3
#pylint: disable=W0611:unused-import
import env
import os
import json
import hashlib
from flask import Flask, request, jsonify
from flask_cors import CORS
from config.settings import REGISTRATION_CONTRACT, REGISTRATION_HASH
# Import our services
from services.analytics import init_analytics, get_latest_data, get_all_data
from services.blockchain import initialize_wallet, contract_interaction
from services.verification import process_id_image

# Initialize Flask application
app = Flask(__name__)
WEBHOOK_PORT = 5000

# Configure CORS
origins = ["https://erth.network"]
if os.environ.get("FLASK_ENV") == "development":
    origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

CORS(app, resources={
    r"/api/analytics": {"origins": origins, "methods": ["GET", "OPTIONS"]},
    r"/api/register": {"origins": origins, "methods": ["POST", "OPTIONS"]}
})

# Request size configuration 
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

# Initialize analytics
init_analytics()

# Initialize blockchain connection
wallet = initialize_wallet()

# Helper functions
def generate_hash(data):
    """Generate SHA-256 hash from dictionary data"""
    return hashlib.sha256(json.dumps(data).encode()).hexdigest()

# Request logging middleware
@app.before_request
def log_request_info():
    if request.path == "/api/register":
        print("Incoming /api/register request")
        if request.is_json:
            print(f"Request body size: {len(json.dumps(request.json)) / 1024 / 1024:.2f} MB")

# API Routes
@app.route("/api/analytics", methods=["GET"])
def analytics():
    """Get analytics data"""
    latest = get_latest_data()
    history = get_all_data()
    return jsonify({"latest": latest, "history": history})

@app.route("/api/register", methods=["POST"])
def register():
    """Register a new user with ID verification"""
    data = request.json
    address = data.get("address")
    id_image = data.get("idImage")
    referred_by = data.get("referredBy")
    
    if not address or not id_image:
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        # Process ID image with SecretAI
        verification_result = process_id_image(id_image)
        success = verification_result.get("success", False)
        identity = verification_result.get("identity", {})
        is_fake = verification_result.get("is_fake", True)
        fake_reason = verification_result.get("fake_reason")
        
        if not success:
            return jsonify({
                "error": "Identity verification failed",
                "is_fake": is_fake,
                "reason": fake_reason or "Unable to verify identity"
            }), 400
        
        # Prepare message for blockchain interaction
        message_object = {
            "register": {
                "address": address,
                "id_hash": generate_hash(identity),
                "affiliate": referred_by or None
            }
        }
        
        # Interact with blockchain contract
        response = contract_interaction(
            wallet=wallet,
            contract_address=REGISTRATION_CONTRACT,
            code_hash=REGISTRATION_HASH,
            message=message_object
        )
        
        # Check response code (equivalent to resp.code === 0 in the JS version)
        if response.get("code") == 0:
            return jsonify({
                "success": True,
                "hash": message_object["register"]["id_hash"],
                "response": response
            })
        else:
            return jsonify({
                "error": "Contract interaction failed",
                "response": response
            }), 400
            
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=WEBHOOK_PORT)