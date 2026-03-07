import streamlit as st

def apply_styles():

    st.markdown("""
    <style>

    /* ===============================
       APP BACKGROUND
    =============================== */

    .stApp {
        background: linear-gradient(135deg,#0F0726,#1A0F3D,#3B0764);
    }

    /* ===============================
       SIDEBAR
    =============================== */

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg,#140B34,#0F0726);
    }

    /* Sidebar navigation items */

    [data-testid="stSidebarNav"] a{
        border-radius:10px;
        padding:10px 12px;
        margin-bottom:6px;
        transition: all 0.2s ease;
    }

    [data-testid="stSidebarNav"] a:hover{
        background: rgba(255,255,255,0.08);
        transform: translateX(5px);
    }

    /* ===============================
       KPI GLASS CARDS
    =============================== */

    div[data-testid="stMetric"]{
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border-radius:16px;
        padding:20px;

        border:1px solid rgba(255,255,255,0.1);
        border-left:4px solid #22D3EE;

        box-shadow:0 10px 30px rgba(0,0,0,0.35);
        transition:all 0.25s ease;
    }

    div[data-testid="stMetric"]:hover{
        transform: translateY(-6px) scale(1.03);
        box-shadow:0 20px 45px rgba(0,0,0,0.6);
        border-left:4px solid #EC4899;
    }

    /* ===============================
       CHART CONTAINER CARDS
    =============================== */

    [data-testid="stPlotlyChart"]{
        background: rgba(255,255,255,0.03);
        padding:20px;
        border-radius:16px;
        box-shadow:0 8px 25px rgba(0,0,0,0.35);
        margin-bottom:20px;
    }

    /* ===============================
       INPUT FIELD STYLING
    =============================== */

    div[data-baseweb="input"]{
        background-color:#1A0F3D;
        border-radius:10px;
        border:1px solid rgba(255,255,255,0.1);
        color:white;
    }

    /* ===============================
       BUTTON STYLING
    =============================== */

    .stButton button{
        background: linear-gradient(90deg,#8B5CF6,#EC4899);
        border:none;
        border-radius:10px;
        color:white;
        font-weight:600;
    }

    .stButton button:hover{
        background: linear-gradient(90deg,#9333EA,#F472B6);
    }

    </style>
    """, unsafe_allow_html=True)