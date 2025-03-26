# 🌿 **SmartCity+ – Sustainable Smart City Solution**

♻️ *Waste segregation with Green Points*  
🚦 *Traffic insights & eco-friendly suggestions*  
🌫 *Real-time AQI monitoring & rewards*  
📊 *Admin dashboard for city insights*  
---

### ✅ **Tech Stack**
- **Frontend:** Streamlit (UI & Navigation)  
- **Database:** SQLite (User authentication & data storage)  
- **Backend:** Python (Modular architecture)  
- **Multithreading:** For parallel execution of waste segregation tasks  

---

### 🚀 **Features**
1. **User Authentication:**  
   - Login and Sign-up with admin and user roles.  
   - Admins access the **Admin Dashboard** with city-wide insights.  

2. **Waste Segregation Module:**  
   - Asynchronous execution for improved performance.  
   - Displays waste management insights and rewards.  

3. **Public Transport Module:**  
   - Displays public transport options and breakdown suggestions.  
   - Provides **eco-friendly recommendations** with Green Points rewards.  

4. **Admin Dashboard:**  
   - Admin-only section for managing city data and monitoring user activity.  

---

### ⚙️ **How to Run Locally**

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/SmartCityPlus.git  
cd SmartCityPlus
```

2. **Install Dependencies**
```bash
pip install streamlit streamlit_option_menu sqlite3
```

3. **Run the App**
```bash
streamlit run main.py
```

---

### 🔥 **Code Architecture**
- `main.py`: The main Streamlit app with navigation and module execution.  
- `Login.py`: Handles user login.  
- `SignUp.py`: Manages user registration.  
- `AdminDashboard.py`: Admin panel for monitoring.  
- `PublicTransport.py`: Displays transport options and suggestions.  
- `WasteSegregation.py`: Manages waste segregation with asynchronous execution.  
- `users.db`: SQLite database for user authentication and data storage.  
