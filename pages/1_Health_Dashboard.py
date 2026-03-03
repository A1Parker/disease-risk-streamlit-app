import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(layout="wide")
# ====== beautification ========
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

# ========


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
# ============ beautification for kpis ======
avg_risk = df["risk_probability"].mean() * 100
avg_bmi = df["bmi"].mean()
avg_chol = df["cholesterol"].mean()


risk_color = "#EF4444" if avg_risk > 60 else "#F59E0B" if avg_risk > 35 else "#10B981"
bmi_color = "#EF4444" if avg_bmi > 30 else "#22D3EE"
chol_color = "#EF4444" if avg_chol > 240 else "#22D3EE"

# ================= KPI ROW =================
st.markdown("## Kpis")
st.markdown("")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Population", f"{len(df):,}")
col2.metric("Avg BMI", f"{avg_bmi:.2f}")
col3.metric("Avg Sugar Intake", f"{df['sugar_intake'].mean():.2f}")
col4.metric("Avg Disease Risk %", f"{avg_risk:.2f}%")

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