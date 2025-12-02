from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-to-something-random'  # Change this!

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
def login_page():
    if 'logged_in' in session:
        return redirect('/grading')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Dummy login - accepts any input
    if username and password:
        session['logged_in'] = True
        session['username'] = username
        return redirect('/grading')
    else:
        flash('Please enter both username and password.')
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect('/')
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    db.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    if 'logged_in' not in session:
        return redirect('/')
    
    name = request.form['name']
    email = request.form['email']
    class_name = request.form['class']
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, class) VALUES (%s, %s, %s)",
        (name, email, class_name)
    )
    db.commit()
    db.close()
    return redirect('/dashboard')

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    if 'logged_in' not in session:
        return redirect('/')
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    db.close()
    return redirect('/dashboard')

@app.route('/grading')
def grading():
    if 'logged_in' not in session:
        return redirect('/')
    return render_template('grading.html')

@app.route('/submit_grade', methods=['POST'])
def submit_grade():
    if 'logged_in' not in session:
        return redirect('/')
    
    student_name = request.form['student_name']
    eye_contact = request.form['eye_contact']
    voice_projection = request.form['voice_projection']
    content_quality = request.form['content_quality']
    body_language = request.form['body_language']
    time_management = request.form['time_management']
    comments = request.form['comments']
    
    total_score = int(eye_contact) + int(voice_projection) + int(content_quality) + int(body_language) + int(time_management)
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """INSERT INTO speech_grades 
        (student_name, eye_contact, voice_projection, content_quality, body_language, time_management, total_score, comments) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (student_name, eye_contact, voice_projection, content_quality, body_language, time_management, total_score, comments)
    )
    db.commit()
    db.close()
    
    flash('Grade submitted successfully!')
    return redirect('/grading')

if __name__ == '__main__':
    conn = get_db_connection()
    app.run(debug=True)
