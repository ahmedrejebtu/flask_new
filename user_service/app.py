from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Database configuration
db_config = {
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'password'),
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'users_db'),
    'raise_on_warnings': True
}

# Establish a database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", 
                       (user_data['username'], user_data['email']))
        conn.commit()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "User created"}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify(user), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
