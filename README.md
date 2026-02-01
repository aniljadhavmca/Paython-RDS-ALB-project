# 🚀 Flask + AWS RDS (MySQL) CRUD Application

This project is a Python Flask web application deployed on EC2 and connected to AWS RDS MySQL (single instance, no replica).
It performs full CRUD operations (Create, Read, Update, Delete) with a simple UI.

---

## 📌 Architecture Overview

Browser → EC2 (Flask App) → AWS RDS MySQL

---

## 📁 Project Structure

python-rds-app/
├── app.py
├── requirements.txt
├── templates/
│   ├── index.html
│   ├── users.html
│   └── edit_user.html
└── static/

---

## 🛠️ Prerequisites

- AWS EC2 instance
- AWS RDS MySQL
- Python 3.8+
- pip installed

Security Groups:
- EC2: Allow HTTP (80)
- RDS: Allow MySQL (3306) from EC2 SG

---

## 🗄️ SQL Commands

### Create Database
CREATE DATABASE testdb;

### Use Database
USE testdb;

### Create Table
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL
);

### Insert Sample Data
INSERT INTO users (name, email) VALUES ('Anil', 'anil@example.com');

---

## ⚙️ Installation Steps
sudo yum install git -y
cd python-rds-app
pip3 install -r requirements.txt
pip install -r requirements.txt

---

## ▶️ Run Application

sudo python3 app.py

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

## 👨‍💻 Author

Created by Anil
