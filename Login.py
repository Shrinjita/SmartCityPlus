import streamlit as st
import sqlite3

def login():
    """User Login Logic"""
    st.subheader("🔑 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Connect to SQLite DB
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            # ✅ Set session state variables
            st.session_state.authenticated = True
            st.session_state.username = username

            st.success("✅ Logged in successfully!")

            # 🔥 Rerun the app to refresh sidebar
            st.experimental_rerun()

        else:
            st.error("❌ Invalid username or password")
