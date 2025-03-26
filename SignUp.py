# SignUp.py
import streamlit as st
import sqlite3

def signup():
    """Sign-Up Module"""

    st.subheader("📝 User Sign-Up")

    # Input fields
    new_username = st.text_input("New Username")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if new_password == confirm_password:
            # Connect to database
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            # Check if the username or email already exists
            cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (new_username, new_email))
            existing_user = cursor.fetchone()

            if existing_user:
                st.error("Username or Email already exists. Please choose a different one.")
            else:
                # Insert new user
                cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                               (new_username, new_email, new_password))
                conn.commit()
                st.success("Sign-up successful! You can now log in.")
            
            conn.close()
        else:
            st.error("Passwords do not match.")
