# user_service/db.py

import mysql.connector
import os

# Database configuration
def get_db_connection():
    db_config = {
        'user': os.environ.get('DB_USER', 'app_user'),
        'password': os.environ.get('DB_PASSWORD', 'password'),
        # Use the environment variable for the database IP address
        'host': os.environ.get('DB_HOST', '172.20.0.4'),
        'database': os.environ.get('DB_NAME', 'microservices_db'),
        'raise_on_warnings': True
    }
    return mysql.connector.connect(**db_config)

def create_user(username, email):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()
