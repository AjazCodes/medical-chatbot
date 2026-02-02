import sqlite3
import hashlib
import json
import os

DB_FILE = "medibot.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (email TEXT PRIMARY KEY, password TEXT)''')
    
    # Profiles table
    c.execute('''CREATE TABLE IF NOT EXISTS profiles
                 (email TEXT PRIMARY KEY, profile_data TEXT,
                  FOREIGN KEY(email) REFERENCES users(email))''')
    
    # History table
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  email TEXT, role TEXT, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(email) REFERENCES users(email))''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(email, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(email, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE email=?", (email,))
    result = c.fetchone()
    conn.close()
    if result and result[0] == hash_password(password):
        return True
    return False

def save_user_profile(email, profile_data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    profile_json = json.dumps(profile_data)
    c.execute("INSERT OR REPLACE INTO profiles (email, profile_data) VALUES (?, ?)", (email, profile_json))
    conn.commit()
    conn.close()

def get_user_profile(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT profile_data FROM profiles WHERE email=?", (email,))
    result = c.fetchone()
    conn.close()
    if result:
        return json.loads(result[0])
    return {}

def save_chat_message(email, role, content):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO history (email, role, content) VALUES (?, ?, ?)", (email, role, content))
    conn.commit()
    conn.close()

def get_chat_history(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT role, content FROM history WHERE email=? ORDER BY timestamp ASC", (email,))
    rows = c.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]

def clear_chat_history(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM history WHERE email=?", (email,))
    conn.commit()
    conn.close()

# Initialize the DB on import
init_db()
