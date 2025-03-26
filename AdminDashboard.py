import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# --------------------------
# 🌟 DATABASE CONNECTION
# --------------------------
def connect_db():
    """Connect to SQLite database."""
    conn = sqlite3.connect("users.db")
    return conn

# --------------------------
# 🌟 AUTHENTICATE ADMIN
# --------------------------
def is_admin(username):
    """Check if the current user is admin."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    return user and user[1] == "Shrinjita" and user[2] == "shrinjitapaul@gmail.com"


# --------------------------
# 🌟 ADMIN DASHBOARD
# --------------------------
def admin_dashboard():
    """Admin Dashboard with Restricted Access"""
    
    # Verify admin credentials
    if "authenticated" in st.session_state and is_admin(st.session_state.get("username", "")):

        # Display the Admin Dashboard
        st.title("📊 Admin Dashboard")
        st.markdown("**Real-time waste segregation statistics**")

        # Sample Waste Data
        data = {
            "Date": pd.date_range(start="2025-03-01", periods=10, freq="D"),
            "Plastic Waste (kg)": [10, 15, 18, 12, 14, 20, 17, 19, 13, 11],
            "Organic Waste (kg)": [30, 35, 32, 28, 26, 34, 31, 36, 29, 27],
            "Metal Waste (kg)": [5, 8, 7, 6, 4, 7, 9, 10, 5, 6]
        }

        df = pd.DataFrame(data)

        # Line Chart - Waste Trends
        fig = px.line(
            df, x="Date", 
            y=["Plastic Waste (kg)", "Organic Waste (kg)", "Metal Waste (kg)"],
            labels={"value": "Waste (kg)", "variable": "Waste Type"},
            title="Daily Waste Segregation"
        )
        st.plotly_chart(fig)

        # Data Table
        st.subheader("📋 Detailed Waste Data")
        st.dataframe(df)

        # Waste Summary Metrics
        st.subheader("📊 Waste Summary Metrics")
        col1, col2, col3 = st.columns(3)

        col1.metric("Plastic Waste", f"{df['Plastic Waste (kg)'].sum()} kg")
        col2.metric("Organic Waste", f"{df['Organic Waste (kg)'].sum()} kg")
        col3.metric("Metal Waste", f"{df['Metal Waste (kg)'].sum()} kg")

    else:
        # Restricted Access Message
        st.warning("Admin access only!")

# --------------------------
# 🌟 STREAMLIT UI
# --------------------------
if __name__ == "__main__":
    admin_dashboard()
