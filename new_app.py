from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# --- Database Configuration ---
DB_CONFIG = {
    'host': '127.0.0.1', # Use '127.0.0.1' if Flask is on the host machine
    'database': 'my_application_db',
    'user': 'root',
    'password': 'helloworld', # Replace with your actual password
    'port': 3306
}

def get_db_connection():
    """Establishes a new database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("Successfully connected to MySQL database")
            return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def home():
    return "Flask app connected to MySQL!"

@app.route('/users')
def list_users():
    """Fetches all users from the USERS table."""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    users_list = []
    try:
        cursor = conn.cursor(dictionary=True) # Use dictionary=True for easier data handling
        # Using the table structure defined previously
        cursor.execute("SELECT userId, fName, lName FROM USERS")
        users = cursor.fetchall()
        users_list = users

    except Error as e:
        print(f"Error executing query: {e}")
        return jsonify({"error": "Error fetching users"}), 500
        
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    return jsonify(users_list)

if __name__ == '__main__':
    # Make sure your MySQL container is running before starting the app
    app.run(debug=True, port=5000)
