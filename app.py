import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #0f172a 0%, #0b1220 100%);
}

.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

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