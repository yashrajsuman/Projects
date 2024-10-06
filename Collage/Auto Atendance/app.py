from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
import cx_Oracle

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(minutes=30)

# Dummy user data for demonstration
users = {
    "admin": "password123"
}

# Database connection function
def get_db_connection():
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='XE') # Update with your DB details
    conn = cx_Oracle.connect(user='system', password='yash123', dsn=dsn_tns)
    return conn

# Fetching data from the database
def fetch_attendance_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    classes = [
        {'name': '4ISEA', 'total': 0, 'present': 0},
        {'name': '4ISEB', 'total': 0, 'present': 0},
        {'name': '4CSDS', 'total': 0, 'present': 0},
        {'name': '2ISEA', 'total': 0, 'present': 0},
        {'name': '2ISEB', 'total': 0, 'present': 0}
    ]
    
    usn_ranges = {
        '4ISEA': ('1AT22IS001', '1AT22IS063'),
        '4ISEB': ('1AT22IS064', '1AT22IS123'),
        '4CSDS': ('1AT22CD001', '1AT22IS063'),
        '2ISEA': ('1AT23IS001', '1AT23IS063'),
        '2ISEB': ('1AT23IS064', '1AT23IS123')
    }
    
    for cls in classes:
        class_name = cls['name']
        usn_range = usn_ranges[class_name]
        
        # Fetch total students
        cursor.execute(f"SELECT COUNT(*) FROM student WHERE USN BETWEEN '{usn_range[0]}' AND '{usn_range[1]}'")
        total_students = cursor.fetchone()[0]
        cls['total'] = total_students
        print(f"Class: {class_name}, Total Students Query: SELECT COUNT(*) FROM student WHERE USN BETWEEN '{usn_range[0]}' AND '{usn_range[1]}'")
        print(f"Total Students: {total_students}")
        
        # Fetch present students for DBMS
        cursor.execute(f"SELECT COUNT(*) FROM attendance WHERE USN BETWEEN '{usn_range[0]}' AND '{usn_range[1]}' AND DBMS = 'P'")
        present_students = cursor.fetchone()[0]
        cls['present'] = present_students
        print(f"Class: {class_name}, Present Students Query: SELECT COUNT(*) FROM attendance WHERE USN BETWEEN '{usn_range[0]}' AND '{usn_range[1]}' AND DBMS = 'P'")
        print(f"Present Students: {present_students}")

        # Debug prints
        print(f"Class: {class_name}, Total: {cls['total']}, Present: {cls['present']}")
    
    cursor.close()
    conn.close()
    
    return classes

@app.route('/')
def home():
    if "user" in session:
        username = session["user"]
        classes = fetch_attendance_data()
        
        overall_percentages = []
        for cls in classes:
            if cls['total'] > 0:
                percentage = (cls['present'] / cls['total']) * 100
            else:
                percentage = 0
            overall_percentages.append(percentage)

        return render_template('index.html', classes=classes, overall_percentages=overall_percentages, username=username)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session.permanent = True
            session["user"] = username
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials, please try again.", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop("user", None)
    flash("You have been logged out!", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
