# SignUp.py
import streamlit as st
import sqlite3
import hashlib
import re

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(str.encode(password)).hexdigest()

def is_valid_email(email):
    """Check if email is valid."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def signup():
    """Sign-Up Module with improved validation and security"""

    st.subheader("📝 User Sign-Up")

    # Input fields
    new_username = st.text_input("New Username")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        # Basic validation
        if not (new_username and new_email and new_password and confirm_password):
            st.error("Please fill in all fields")
            return
            
        if not is_valid_email(new_email):
            st.error("Please enter a valid email address")
            return
            
        if len(new_password) < 8:
            st.error("Password must be at least 8 characters long")
            return
            
        if new_password != confirm_password:
            st.error("Passwords do not match")
            return
            
        # Hash the password
        hashed_password = hash_password(new_password)
        
        try:
            # Connect to database
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            # Check if the username or email already exists
            cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (new_username, new_email))
            existing_user = cursor.fetchone()

            if existing_user:
                st.error("Username or Email already exists. Please choose a different one.")
            else:
                # Insert new user with hashed password
                cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                               (new_username, new_email, hashed_password))
                conn.commit()
                st.success("Sign-up successful! You can now log in.")
            
            conn.close()
        except sqlite3.Error as e:
            st.error(f"Database error: {e}")