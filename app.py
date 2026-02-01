from flask import Flask, render_template, request, redirect
import mysql.connector
import sys

app = Flask(__name__)

# =======================
# RDS DATABASE CONNECTION
# =======================
try:
    db = mysql.connector.connect(
        host="testdb.cabgooyqiqf5.us-east-1.rds.amazonaws.com",
        user="admin",
        password="DatabaseAnil",
        database="testdb",
        port=3306
    )
    cursor = db.cursor(dictionary=True)
    print("✅ Connected to AWS RDS")
except mysql.connector.Error as err:
    print("❌ RDS connection failed:", err)
    sys.exit(1)

# =======================
# HOME (ADD USER)
# =======================
@app.route('/')
def home():
    return render_template("index.html")

# =======================
# ADD USER
# =======================
@app.route('/add-user', methods=['POST'])
def add_user():
    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        return "Name and Email required"

    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (name, email)
    )
    db.commit()
    return redirect('/users')

# =======================
# LIST USERS
# =======================
@app.route('/users')
def users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template("users.html", users=users)

# =======================
# EDIT USER FORM
# ======
