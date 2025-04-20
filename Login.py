import streamlit as st
import sqlite3
import hashlib

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(str.encode(password)).hexdigest()

def login():
    """User Login Logic with improved security"""
    st.subheader("🔑 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not username or not password:
            st.error("Please enter both username and password")
            return
            
        # Hash the password
        hashed_password = hash_password(password)
        
        try:
            # Connect to SQLite DB
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            # First check if user exists
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if user:
                # Now check password against stored hash
                stored_password = user[3]  # Assuming password is at index 3
                
                if stored_password == hashed_password:
                    # ✅ Set session state variables
                    st.session_state.authenticated = True
                    st.session_state.username = username

                    st.success("✅ Logged in successfully!")

                    # 🔥 Rerun the app to refresh sidebar
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            else:
                st.error("❌ Invalid username or password")
                
        except sqlite3.Error as e:
            st.error(f"Database error: {e}")
        finally:
            conn.close()