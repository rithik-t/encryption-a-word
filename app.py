from flask import Flask, request, jsonify, render_template
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load the key from an environment variable
load_dotenv()
key = os.getenv('ENCRYPTION_KEY')
if not key:
    raise ValueError("Encryption key is missing! Set the ENCRYPTION_KEY in your .env file.")
cipher = Fernet(key)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        data = request.json
        plaintext = data.get("text", "")
        
        if not plaintext:
            return jsonify({"error": "No text provided for encryption!"}), 400
        
        encrypted_text = cipher.encrypt(plaintext.encode()).decode()
        return jsonify({"encrypted": encrypted_text})
    except Exception as e:
        return jsonify({"error": f"Encryption failed: {str(e)}"}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        data = request.json
        encrypted_text = data.get("text", "")
        
        if not encrypted_text:
            return jsonify({"error": "No encrypted text provided!"}), 400
        
        decrypted_text = cipher.decrypt(encrypted_text.encode()).decode()
        return jsonify({"decrypted": decrypted_text})
    except Exception as e:
        return jsonify({"error": f"Decryption failed: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(debug=True)
