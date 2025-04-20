# init_db.py
import sqlite3
import hashlib

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(str.encode(password)).hexdigest()

# Connect to SQLite database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Drop existing table if it exists to reset schema
cursor.execute('DROP TABLE IF EXISTS users')

# Create table to store user information with proper schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Insert sample admin user with hashed password
admin_password_hash = hash_password("password123")
cursor.execute('INSERT OR IGNORE INTO users (username, email, password) VALUES (?, ?, ?)', 
               ('Shrinjita', 'shrinjitapaul@gmail.com', admin_password_hash))

# Commit and close connection
conn.commit()
conn.close()

print("Database initialized successfully!")