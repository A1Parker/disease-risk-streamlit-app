import streamlit as st
from utils.ui_styles import apply_styles
apply_styles()

# Page configuration
st.set_page_config(
    page_title="Disease Risk Prediction System",
    page_icon="🏥",
    layout="wide"
)



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