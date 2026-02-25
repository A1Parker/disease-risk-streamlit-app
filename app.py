import streamlit as st
from utils.auth import login

st.set_page_config(page_title="Disease Risk Prediction System", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
    st.sidebar.success("Logged in as Admin")
    st.title("🏥 Disease Risk Prediction System")
    st.write("Use the sidebar to navigate through dashboards and prediction.")