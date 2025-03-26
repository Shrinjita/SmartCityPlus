import streamlit as st
from streamlit_option_menu import option_menu  # Stylish sidebar navigation
import sqlite3
import threading
import time
from Login import login
from SignUp import signup
from AdminDashboard import admin_dashboard
from PublicTransport import public_transport
from WasteSegregation import waste_segregation

# ---------------------------
# ✅ Efficient SQLite Connection with Caching
# ---------------------------
@st.cache_resource
def connect_db():
    """Cached DB connection to reduce repeated DB calls."""
    conn = sqlite3.connect("users.db", check_same_thread=False)
    return conn

# ---------------------------
# ✅ Admin Authentication Check
# ---------------------------
def is_admin(username):
    """Check if the user is admin without closing the DB connection."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        return user and user[1] == "Shrinjita" and user[2] == "shrinjitapaul@gmail.com"
    
    except sqlite3.ProgrammingError as e:
        st.error(f"Database error: {e}")
        return False

    finally:
        cursor.close()  # ✅ Close the cursor only, not the DB connection
# ---------------------------
# ✅ User Authentication Check
# ---------------------------
def is_logged_in():
    return "authenticated" in st.session_state and st.session_state.authenticated

# ---------------------------
# ✅ Sidebar Navigation with Reduced Latency
# ---------------------------
def sidebar_navigation():
    """Sidebar with role-based navigation."""
    if is_logged_in():
        username = st.session_state.get("username", "")

        # 🎯 Admin Role
        if is_admin(username):
            with st.sidebar:
                st.write(f"👋 Welcome, {username} (Admin)")
                menu = option_menu(
                    menu_title="Navigation",
                    options=["Public Transport", "Waste Segregation", "Admin Dashboard", "Logout"],
                    icons=["bus-front", "recycle", "shield-check", "box-arrow-right"],
                    menu_icon="cast",
                    default_index=0,
                    orientation="vertical"
                )
                return menu

        # 👥 Normal User Role
        else:
            with st.sidebar:
                st.write(f"👋 Welcome, {username}")
                menu = option_menu(
                    menu_title="Navigation",
                    options=["Public Transport", "Waste Segregation", "Logout"],
                    icons=["bus-front", "recycle", "box-arrow-right"],
                    menu_icon="cast",
                    default_index=0,
                    orientation="vertical"
                )
                return menu

    # 🔒 Before Login: Show only Login and Sign Up
    else:
        with st.sidebar:
            st.write("🔒 Please log in to access the platform")
            menu = option_menu(
                menu_title="Navigation",
                options=["Login", "Sign Up"],
                icons=["box-arrow-in-right", "person-plus"],
                menu_icon="cast",
                default_index=0,
                orientation="vertical"
            )
            return menu

# ---------------------------
# 🚀 Asynchronous Waste Segregation
# ---------------------------
def async_waste_segregation():
    """Run waste segregation in a separate thread for faster performance."""
    thread = threading.Thread(target=waste_segregation)
    thread.start()

# ---------------------------
# ✅ Main Function with Parallel Execution
# ---------------------------
def main():

    # Sidebar Navigation
    menu = sidebar_navigation()

    # 🚀 Display modules based on selected menu
    if menu == "Login":
        st.write("🔑 **Login Page**")
        login()

    elif menu == "Sign Up":
        st.write("📝 **Sign Up Page**")
        signup()

    elif menu == "Public Transport":
        st.write("🚍 **Public Transport Module**")
        public_transport()

    elif menu == "Waste Segregation":
        st.write("♻️ **Waste Segregation Module**")
        
        # Run Waste Segregation in a separate thread
        waste_segregation()

    elif menu == "Admin Dashboard" and is_logged_in() and is_admin(st.session_state.get("username", "")):
        st.write("📊 **Admin Dashboard**")
        admin_dashboard()

    elif menu == "Logout":
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.success("✅ Logged out successfully!")

        # 🔥 Rerun app after logout
        time.sleep(1)  
        st.rerun()


# ✅ Run the app
if __name__ == "__main__":
    main()
