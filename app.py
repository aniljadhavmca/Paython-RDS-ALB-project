from flask import Flask, render_template, request, redirect
import mysql.connector
import sys

app = Flask(__name__)

# =================================================
# DATABASE CONNECTIONS
# =================================================

# 🔹 PRIMARY RDS (WRITE)
try:
    primary_db = mysql.connector.connect(
        host="testdb.cabgooyqiqf5.us-east-1.rds.amazonaws.com",
        user="admin",
        password="DatabaseAnil",
        database="testdb",
        port=3306
    )
    primary_cursor = primary_db.cursor(dictionary=True)
    print("✅ Connected to PRIMARY RDS")
except mysql.connector.Error as err:
    print("❌ Primary DB error:", err)
    sys.exit(1)

# 🔹 READ REPLICA (READ)
try:
    replica_db = mysql.connector.connect(
        host="testdb-read-replica.cabgooyqiqf5.us-east-1.rds.amazonaws.com",
        user="admin",
        password="DatabaseAnil",
        database="testdb",
        port=3306
    )
    replica_cursor = replica_db.cursor(dictionary=True)
    print("✅ Connected to READ REPLICA")
except mysql.connector.Error as err:
    print("❌ Replica DB error:", err)
    sys.exit(1)

# =================================================
# HOME – ADD USER
# =================================================
@app.route('/')
def home():
    return render_template("index.html")

# =================================================
# ADD USER (WRITE → PRIMARY)
# =================================================
@app.route('/add-user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    email = request.form.get('email')

    primary_cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (name, email)
    )
    primary_db.commit()

    # IMPORTANT: read from PRIMARY to avoid replica lag
    return redirect('/users?source=primary')

# =================================================
# USERS LIST (READ → SMART ROUTING)
# =================================================
@app.route('/users')
def users():
    search = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    source = request.args.get('source', 'replica')
    limit = 5
    offset = (page - 1) * limit

    cursor = primary_cursor if source == 'primary' else replica_cursor

    # COUNT
    if search:
        cursor.execute(
            "SELECT COUNT(*) AS total FROM users WHERE name LIKE %s OR email LIKE %s",
            (f"%{search}%", f"%{search}%")
        )
    else:
        cursor.execute("SELECT COUNT(*) AS total FROM users")

    total = cursor.fetchone()['total']
    total_pages = (total + limit - 1) // limit

    # FETCH DATA
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

# =================================================
# EDIT USER (READ → REPLICA)
# =================================================
@app.route('/edit-user/<int:user_id>')
def edit_user(user_id):
    replica_cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = replica_cursor.fetchone()
    return render_template("edit_user.html", user=user)

# =================================================
# UPDATE USER (WRITE → PRIMARY)
# =================================================
@app.route('/update-user', methods=['POST'])
def update_user():
    primary_cursor.execute(
        "UPDATE users SET name=%s, email=%s WHERE id=%s",
        (request.form['name'], request.form['email'], request.form['id'])
    )
    primary_db.commit()

    return redirect('/users?source=primary')

# =================================================
# DELETE USER (WRITE → PRIMARY)
# =================================================
@app.route('/delete-user/<int:user_id>')
def delete_user(user_id):
    primary_cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    primary_db.commit()

    return redirect('/users?source=primary')

# =================================================
# HEALTH CHECK
# =================================================
@app.route('/health')
def health():
    return "OK", 200

# =================================================
# START SERVER
# =================================================
if __name__ == "__main__":
    print("🚀 Flask app running with RDS Read Replica")
    app.run(host="0.0.0.0", port=80, debug=True)
