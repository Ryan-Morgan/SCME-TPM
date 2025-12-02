from flask import Flask, render_template, request, redirect
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Connect to your database
DB_CONFIG = {
    'host': '127.0.0.1', # Use '127.0.0.1' if Flask is on the host machine
    'database': 'my_application_db',
    'user': 'root',
    'password': 'my-secret-pw', # Replace with your actual password
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
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    class_name = request.form['class']
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, class) VALUES (%s, %s, %s)",
        (name, email, class_name)
    )
    db.commit()
    return redirect('/')


@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    return redirect('/')

if __name__ == '__main__':
    conn = get_db_connection()
    app.run(debug=True)
