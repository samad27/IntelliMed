import mysql.connector
import streamlit as st

# ✅ DB Config — replace with your MySQL credentials
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "Samad@2702"  # <== CHANGE THIS
MYSQL_DB = "intellimed_db"

# ✅ Initialize DB and create tables
def init_db():
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
    cursor.close()
    conn.close()

    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    cursor = conn.cursor()

    # Users table with 'created_at' column added
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('admin', 'user') NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Scan logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100),
            scan_type VARCHAR(50),
            result TEXT,
            confidence FLOAT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    # Default users (no changes here)
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'adminpass', 'admin')")
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'user1'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('user1', 'userpass', 'user')")

    conn.commit()
    cursor.close()
    conn.close()

# DB connection
def connect_db():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

# Login
def login(username, password, role):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s AND role=%s", (username, password, role))
    result = cursor.fetchone()
    conn.close()
    return result

# Register new user
def register_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, 'user')", (username, password))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    finally:
        conn.close()

# Login Form
def login_form(role):
    st.subheader(f"{role.capitalize()} Login")
    username = st.text_input("Username", key=f"{role}_user")
    password = st.text_input("Password", type="password", key=f"{role}_pass")
    if st.button("Login", key=f"{role}_login_btn"):
        if login(username, password, role):
            st.session_state['logged_in'] = True
            st.session_state['role'] = role
            st.session_state['username'] = username
            st.success(f"Welcome {username} ({role})")
        else:
            st.error("Invalid credentials")

# Registration Form
def registration_form():
    st.subheader("User Registration")
    username = st.text_input("Choose a Username", key="reg_user")
    password = st.text_input("Choose a Password", type="password", key="reg_pass")
    if st.button("Create Account", key="create_account_button"):
        if register_user(username, password):
            st.success("Registration successful! You can now login.")
        else:
            st.error("Username already exists. Try another one.")



#333
def log_scan_result(username, scan_type, result, confidence):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO scan_logs (username, scan_type, result, confidence) VALUES (%s, %s, %s, %s)",
        (username, scan_type, result, confidence)
    )
    conn.commit()
    conn.close()
