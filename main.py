import streamlit as st
import sqlite3
import threading
import time
from Login import login
from SignUp import signup
from AdminDashboard import admin_dashboard
from PublicTransport import public_transport
from WasteSegregation import waste_segregation

# Add missing import
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(
    page_title="EcoChennai Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        # Changed index from 1 and 2 to 0 and 1 to match the query results
        return user and user[0] == "Shrinjita" and user[1] == "shrinjitapaul@gmail.com"
    
    except sqlite3.Error as e:
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
    with st.sidebar:
        if is_logged_in():
            username = st.session_state.get("username", "")

            # 🎯 Admin Role
            if is_admin(username):
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
# ✅ Main Function with Improved Error Handling
# ---------------------------
def main():
    # Apply custom CSS
    try:
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # Ignore if file not found

    # Sidebar Navigation
    menu = sidebar_navigation()

    # 🚀 Display modules based on selected menu
    if menu == "Login":
        login()

    elif menu == "Sign Up":
        signup()

    elif menu == "Public Transport" and is_logged_in():
        public_transport()

    elif menu == "Waste Segregation" and is_logged_in():
        waste_segregation()

    elif menu == "Admin Dashboard" and is_logged_in() and is_admin(st.session_state.get("username", "")):
        admin_dashboard()

    elif menu == "Logout" and is_logged_in():
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.success("✅ Logged out successfully!")

        # 🔥 Rerun app after logout
        time.sleep(1)  
        st.rerun()
    
    # Handle unauthorized access attempts
    elif menu in ["Public Transport", "Waste Segregation", "Admin Dashboard"] and not is_logged_in():
        st.warning("Please log in to access this feature")


# ✅ Run the app
if __name__ == "__main__":
    main()