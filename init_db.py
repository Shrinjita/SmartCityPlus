# init_db.py
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create table to store user information
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Insert sample users (optional)
cursor.execute('INSERT OR IGNORE INTO users (username, email, password) VALUES (?, ?, ?)', 
               ('Shrinjita', 'shrinjitapaul@gmail.com', 'password123'))

# Commit and close connection
conn.commit()
conn.close()

print("Database initialized successfully!")
