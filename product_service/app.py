from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Database configuration
db_config = {
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'password'),
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'products_db'),
    'raise_on_warnings': True
}

# Establish a database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    update_data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE products SET name = %s, price = %s WHERE id = %s", 
                       (update_data['name'], update_data['price'], product_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Product not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Product updated"}), 200

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Product not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Product deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
