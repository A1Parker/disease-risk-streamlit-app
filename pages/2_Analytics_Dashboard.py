import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(layout="wide")
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
col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg Stress Level", round(df["stress_level"].mean(), 2))
col2.metric("Avg Physical Activity", round(df["physical_activity"].mean(), 2))
col3.metric("Avg Sleep Hours", round(df["sleep_hours"].mean(), 2))
col4.metric("Avg Mental Health Score", round(df["mental_health_score"].mean(), 2))

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