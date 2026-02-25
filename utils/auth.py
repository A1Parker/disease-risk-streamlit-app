import streamlit as st

def login():
    st.title("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "health123":
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid credentials")

    return st.session_state.get("authenticated", False)