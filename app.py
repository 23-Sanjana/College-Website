from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication
bcrypt = Bcrypt(app)

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Your MySQL username
    password="Xyz@123",  # Your MySQL password
    database="user_auth"
)
cursor = db.cursor()

# User Registration Route (No Role)
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                       (name, email, hashed_password))
        db.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400

# User Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    cursor.execute("SELECT id, name, password FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and bcrypt.check_password_hash(user[2], password):
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user[0],
                "name": user[1]
            }
        })
    else:
        return jsonify({"error": "Invalid email or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)