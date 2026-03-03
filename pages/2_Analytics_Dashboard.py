import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(layout="wide")
#==
st.markdown("""
<style>

/* Sidebar background */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #0b1220 100%);
}

/* Sidebar section title (Filters) */
section[data-testid="stSidebar"] h2 {
    color: #FFFFFF !important;
}

/* Multiselect label text (Gender, Job Type, Occupation) */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    color: #FFFFFF !important;
}

/* Make the dropdown container slightly lighter */
section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background-color: #111827 !important;
}

/* Selected tags */
section[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background-color: #22D3EE !important;
    color: black !important;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(30,41,59,0.6), rgba(15,23,42,0.8));
    padding: 20px;
    border-radius: 18px;
    border-left: 5px solid #22D3EE;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    transition: transform 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
}

div[data-testid="stMetric"] label {
    color: #94A3B8 !important;
    font-size: 10px !important;
}

div[data-testid="stMetric"] div {
    color: white !important;
    font-size: 20px !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)



#====

df = load_data()

# ================= SIDEBAR FILTERS =================
st.sidebar.header("🔎 Filters")

gender_filter = st.sidebar.multiselect(
    "Gender",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

job_filter = st.sidebar.multiselect(
    "Job Type",
    options=df["job_type"].unique(),
    default=df["job_type"].unique()
)

occupation_filter = st.sidebar.multiselect(
    "Occupation",
    options=df["occupation"].unique(),
    default=df["occupation"].unique()
)


# Apply Filters
df = df[
    (df["gender"].isin(gender_filter)) &
    (df["job_type"].isin(job_filter)) &
    (df["occupation"].isin(occupation_filter))
]

st.title("📈 Advanced Health Analytics")

# ================= KPI ROW =================
st.markdown("### Key Behavioral Metrics")
st.markdown("")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg Stress Level", f"{df['stress_level'].mean():.2f}")
col2.metric("Avg Physical Activity", f"{df['physical_activity'].mean():.2f}")
col3.metric("Avg Sleep Hours", f"{df['sleep_hours'].mean():.2f}")
col4.metric("Avg Mental Health Score", f"{df['mental_health_score'].mean():.2f}")

st.divider()

# ================= HEALTHY VS DISEASE =================
fig = px.pie(
    df,
    names="model_prediction",
    hole=0.6,
    title="Healthy vs Diseased Distribution"
)
st.plotly_chart(fig, use_container_width=True)

# ================= BMI VS HEALTH =================
fig = px.bar(
    df.groupby(["bmi_category", "model_prediction"]).size().reset_index(name="count"),
    x="bmi_category",
    y="count",
    color="model_prediction",
    barmode="group",
    title="BMI Distribution by Health Status"
)
st.plotly_chart(fig, use_container_width=True)

# ================= STRESS VS RISK SCORE =================
fig = px.bar(
    df.groupby("risk_score")["stress_level"].mean().reset_index(),
    x="risk_score",
    y="stress_level",
    title="Stress Level Distribution by Risk Score"
)
st.plotly_chart(fig, use_container_width=True)

# ================= SLEEP VS RISK =================
fig = px.bar(
    df.groupby("risk_score")["sleep_hours"].mean().reset_index(),
    x="risk_score",
    y="sleep_hours",
    title="Sleep Hours Effect on Risk Score"
)
st.plotly_chart(fig, use_container_width=True)

# ================= DAILY STEPS VS RISK =================
fig = px.bar(
    df.groupby("risk_score")["daily_steps"].mean().reset_index(),
    x="risk_score",
    y="daily_steps",
    title="Daily Steps vs Risk Score"
)
st.plotly_chart(fig, use_container_width=True)