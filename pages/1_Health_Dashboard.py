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

st.title("📊 Health Overview Dashboard")

# ================= KPI ROW =================
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Population", f"{len(df):,}")
col2.metric("Avg BMI", round(df["bmi"].mean(), 2))
col3.metric("Avg Sugar Intake", round(df["sugar_intake"].mean(), 2))
col4.metric("Avg Disease Risk %", round(df["risk_probability"].mean()*100, 2))
col5.metric("Avg Cholesterol", round(df["cholesterol"].mean(), 2))

st.divider()

# ================= AGE GROUP DONUT =================
col1, col2, col3 = st.columns(3)

with col1:
    fig = px.pie(
        df,
        names="age_group",
        hole=0.6,
        title="Age Group Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= ALCOHOL CONSUMPTION =================
alcohol_df = df["alcohol_consumption"].value_counts().reset_index()
alcohol_df.columns = ["alcohol_consumption", "count"]

fig = px.bar(
    alcohol_df,
    x="alcohol_consumption",
    y="count",
    title="Alcohol Consumption"
)

st.plotly_chart(fig, use_container_width=True)

with col3:
    fig = px.pie(
        df,
        names="bmi_category",
        hole=0.6,
        title="BMI Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ================= HEALTH CONDITION BY AGE =================
fig = px.bar(
    df.groupby(["age_group", "model_prediction"]).size().reset_index(name="count"),
    x="age_group",
    y="count",
    color="model_prediction",
    barmode="group",
    title="Health Condition Among Age Group"
)
st.plotly_chart(fig, use_container_width=True)

# ================= SMOKER DISTRIBUTION =================
fig = px.pie(
    df,
    names="smoking_level",
    hole=0.6,
    title="Smoker Distribution"
)
st.plotly_chart(fig, use_container_width=True)