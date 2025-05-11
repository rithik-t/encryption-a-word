from flask import Flask, request, jsonify, render_template
from cryptography.fernet import Fernet

app = Flask(__name__)

# Generate a key (save this for real use)
key = Fernet.generate_key()
cipher = Fernet(key)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    plaintext = data.get("text", "")
    encrypted_text = cipher.encrypt(plaintext.encode()).decode()
    return jsonify({"encrypted": encrypted_text})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    encrypted_text = data.get("text", "")
    try:
        decrypted_text = cipher.decrypt(encrypted_text.encode()).decode()
        return jsonify({"decrypted": decrypted_text})
    except:
        return jsonify({"error": "Invalid encrypted text!"})

if __name__ == '__main__':
    app.run(debug=True)
