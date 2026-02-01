# 🚀 Flask + AWS RDS (MySQL) CRUD Application

This project is a Python Flask web application deployed on EC2 and connected to AWS RDS MySQL (single instance, no replica).
It performs full CRUD operations (Create, Read, Update, Delete) with a simple UI.

---

## 📌 Architecture Overview

Browser → EC2 (Flask App) → AWS RDS MySQL

---


## ✨ Features

- Add new users
- View users list
- Edit existing users
- Delete users
- Search Users
- Paginations
- Health check endpoint (`/health`)

---

## 🧰 Technology Stack

- **Backend**: Python, Flask
- **Database**: AWS RDS (MySQL)
- **Server**: AWS EC2
- **UI**: HTML, CSS
- **OS**: Amazon Linux

---

## 📁 Project Structure

```text
Paython-RDS-ALB-project/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
│
├── templates/             # HTML templates (Jinja2)
│   ├── index.html         # Add User page
│   ├── users.html         # View Users page
│   └── edit_user.html     # Edit User page
│
└── static/                # Static assets
    └── css/
        └── style.css      # Application CSS
```
---

## 🛠️ Prerequisites

- AWS EC2 instance
- AWS RDS MySQL
- Python 3.8+
- pip3 installed

Security Groups:
- EC2: Allow HTTP (80)
- RDS: Allow MySQL (3306) from EC2 SG

---

## 🗄️ SQL Commands

### Create Database
- CREATE DATABASE testdb;

### Use Database
- USE testdb;

### Create Table
- CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL
);

### Insert Sample Data
- INSERT INTO users (name, email) VALUES ('Anil', 'anil@example.com');

---

## ⚙️ Installation Steps
- sudo yum install git -y
- cd python-rds-app
- pip3 install -r requirements.txt

---

## ▶️ Run Application

- sudo python3 app.py

---

## 🌐 URLs

/           → Add User  
/users      → List Users  
/health     → Health Check  

---

## 🎯 Highlights

- Flask + MySQL
- AWS RDS integration
- Full CRUD
- Interview-ready project

---

## ❗ What’s happening (VERY IMPORTANT)
```pgsql
ADD USER (WRITE)
   ↓
PRIMARY RDS ✅ (data saved immediately)

VIEW USERS (READ)
   ↓
READ REPLICA ❌ (data not visible immediately)

Step 1: Add FIRST record
Now when you open /users (reading from replica):
Replica has not caught up yet
So user1 is NOT visible

Step 2: Add SECOND record
INSERT user2
→ PRIMARY RDS ✅
→ REPLICA sync starts again

During this time:
Replica finally receives previous changes
So now it contains:
user1 ✅
(maybe user2 after a moment)

👉 That’s why user1 suddenly appears after adding user2
```

---

##  🧠 Why this happens (Simple Explanation)

- Primary RDS writes data immediately
- Read Replica copies data asynchronously
- There is replication lag
- So immediate reads may not see new data
This is called:
- Read-after-write inconsistency

## 👨‍💻 Author

- Created by Anil
