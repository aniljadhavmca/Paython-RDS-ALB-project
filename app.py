from flask import Flask, render_template, request, redirect
import mysql.connector
import sys

app = Flask(__name__)

try:
    db = mysql.connector.connect(
        host="devdb.cc5ggsic2so9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="DatabaseAnil",
        database="testdb",
        port=3306
    )
    cursor = db.cursor(dictionary=True)
    print("Connected to AWS RDS")
except mysql.connector.Error as err:
    print("RDS connection failed:", err)
    sys.exit(1)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/add-user', methods=['POST'])
def add_user():
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (request.form['name'], request.form['email'])
    )
    db.commit()
    return redirect('/users')

@app.route('/users')
def users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template("users.html", users=users)

@app.route('/edit-user/<int:user_id>')
def edit_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    return render_template("edit_user.html", user=user)

@app.route('/update-user', methods=['POST'])
def update_user():
    cursor.execute(
        "UPDATE users SET name=%s, email=%s WHERE id=%s",
        (request.form['name'], request.form['email'], request.form['id'])
    )
    db.commit()
    return redirect('/users')

@app.route('/delete-user/<int:user_id>')
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.commit()
    return redirect('/users')

@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
