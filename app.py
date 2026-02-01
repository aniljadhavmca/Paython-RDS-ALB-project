from flask import Flask, render_template, request, redirect
import mysql.connector
import sys

app = Flask(__name__)

# =======================
# DATABASE CONNECTION
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
# HOME
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
# USERS (SEARCH + PAGINATION)
# =======================
@app.route('/users')
def users():
    search = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    limit = 5
    offset = (page - 1) * limit

    # Count total users
    if search:
        cursor.execute(
            "SELECT COUNT(*) AS total FROM users WHERE name LIKE %s OR email LIKE %s",
            (f"%{search}%", f"%{search}%")
        )
    else:
        cursor.execute("SELECT COUNT(*) AS total FROM users")

    total = cursor.fetchone()['total']
    total_pages = (total + limit - 1) // limit

    # Fetch users
    if search:
        cursor.execute(
            """SELECT * FROM users
               WHERE name LIKE %s OR email LIKE %s
               ORDER BY id DESC
               LIMIT %s OFFSET %s""",
            (f"%{search}%", f"%{search}%", limit, offset)
        )
    else:
        cursor.execute(
            "SELECT * FROM users ORDER BY id DESC LIMIT %s OFFSET %s",
            (limit, offset)
        )

    users = cursor.fetchall()

    return render_template(
        "users.html",
        users=users,
        page=page,
        total_pages=total_pages,
        search=search
    )

# =======================
# EDIT USER FORM
# =======================
@app.route('/edit-user/<int:user_id>')
def edit_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    return render_template("edit_user.html", user=user)

# =======================
# UPDATE USER
# =======================
@app.route('/update-user', methods=['POST'])
def update_user():
    cursor.execute(
        "UPDATE users SET name=%s, email=%s WHERE id=%s",
        (request.form['name'], request.form['email'], request.form['id'])
    )
    db.commit()
    return redirect('/users')

# =======================
# DELETE USER
# =======================
@app.route('/delete-user/<int:user_id>')
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.commit()
    return redirect('/users')

# =======================
# HEALTH CHECK
# =======================
@app.route('/health')
def health():
    return "OK", 200

# =======================
# START SERVER
# =======================
if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    app.run(host="0.0.0.0", port=80, debug=True)
