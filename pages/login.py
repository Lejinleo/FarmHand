import streamlit as st
import hashlib
import os
import pickle

# --- Page Config ---
st.set_page_config(page_title="Login | Kerala Farming Assistant", page_icon="🔑")

# --- User database storage ---
USER_FILE = "users.pkl"

if os.path.exists(USER_FILE):
    with open(USER_FILE, "rb") as f:
        users = pickle.load(f)
else:
    users = {"admin": hashlib.sha256("admin123".encode()).hexdigest()}

# --- Session State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Password Hash Function ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Save Users to file ---
def save_users():
    with open(USER_FILE, "wb") as f:
        pickle.dump(users, f)

# --- Login Function ---
def login():
    st.title("🔑 Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        hashed = hash_password(password)
        if username in users and users[username] == hashed:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("❌ Invalid username or password")

# --- Signup Function ---
def signup():
    st.title("📝 Signup")
    new_user = st.text_input("Choose Username", key="signup_user")
    new_pass = st.text_input("Choose Password", type="password", key="signup_pass")
    confirm_pass = st.text_input("Confirm Password", type="password", key="signup_confirm")

    if st.button("Signup"):
        if new_user in users:
            st.error("❌ Username already exists")
        elif new_pass != confirm_pass:
            st.error("❌ Passwords do not match")
        elif len(new_pass) < 4:
            st.error("❌ Password too short (min 4 characters)")
        else:
            users[new_user] = hash_password(new_pass)
            save_users()
            st.success("✅ Account created! Please login.")

# --- Authentication Flow ---
if st.session_state.logged_in:
    # --- User is logged in, load main app ---
    import main_app
    main_app.run_app()
else:
    # --- Show Login/Signup options only if not logged in ---
    auth_option = st.radio("Choose Option", ["Login", "Signup"])
    if auth_option == "Login":
        login()
    else:
        signup()
