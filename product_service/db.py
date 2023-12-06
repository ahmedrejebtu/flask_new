# product_service/db.py

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

def update_product(product_id, name, price):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE products SET name = %s, price = %s WHERE id = %s", (name, price, product_id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
