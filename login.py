import streamlit as st
from auth_simple import register_user, login_user

# Function to display login page
def show_login_page():

    # Create three columns to center the content
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        # Custom CSS for clean design
        st.markdown("""
            <style>
            
            .stApp {
                background-image: url("https://media.istockphoto.com/id/1786486973/photo/young-sprout-agricultural-technologies-banner.jpg?s=612x612&w=0&k=20&c=5RCxOczVxCdND-NLRx2LrlaYwnpexMY34by5C0ixL04=");
                background-size: cover;
                background-attachment: fixed;
                background-repeat: no-repeat;
                background-position: center;
            }

            .login-title {
                font-size: 32px;
                font-weight: bold;
                text-align: center;
                color: white;
                margin-bottom: 20px;
            }

            .stTextInput > div > div > input {
                background-color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                color: black;
            }
            .stPasswordInput > div > div > input {
                background-color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;    
            }

            .stButton > button {
                background-color: #008000;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                width: 25%;
                display: block;
                margin: 20px auto;  /* Centers the button horizontally */
            }

            .stSelectbox > div {
                border-radius: 8px;
                width: 40%;
                display: block;
            }
        """, unsafe_allow_html=True)

        # Wrapper: Title
        # st.markdown('<div class="login-title">🌾 AgroVision</div>', unsafe_allow_html=True)
        st.markdown(f"<nav style='background:#008000;padding:5px;text-align:center;color:white;'>"
                f"<h1>{('AgroVision')}</h1></nav>", unsafe_allow_html=True)

        # Dropdown for login or register option
        choice = st.selectbox("Login/Register", ["Login", "Register"])

        if choice == "Login":
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                user = login_user(username, password)
                if user:
                    st.success(f"Welcome back, {username}!")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        elif choice == "Register":
            st.subheader("Register")
            username = st.text_input(" Username")
            password = st.text_input(" Password", type="password")
            if st.button("Register"):
                if register_user(username, password):
                    user = login_user(username, password)
                    if user:
                        st.success(f"Welcome back, {username}!")
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.rerun()
                else:
                    st.error("Username already exists or registration error.")
