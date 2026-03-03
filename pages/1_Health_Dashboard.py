import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
# ====== beautification ========
def metric_card(title, value, accent="#22D3EE"):

    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, rgba(30,41,59,0.6), rgba(15,23,42,0.8));
        padding:22px;
        border-radius:18px;
        border-left: 5px solid {accent};
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.35);
        transition: 0.3s ease-in-out;
    ">
        <p style="
            color:#94A3B8;
            font-size:14px;
            margin-bottom:5px;
            letter-spacing:0.5px;
        ">
            {title}
        </p>

        <h2 style="
            color:white;
            font-size:28px;
            font-weight:600;
            margin:0;
        ">
            {value}
        </h2>
    </div>
    """, unsafe_allow_html=True)

# ========

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
# ============ beautification for kpis ======
avg_risk = df["risk_probability"].mean() * 100
avg_bmi = df["bmi"].mean()
avg_chol = df["cholesterol"].mean()


risk_color = "#EF4444" if avg_risk > 60 else "#F59E0B" if avg_risk > 35 else "#10B981"
bmi_color = "#EF4444" if avg_bmi > 30 else "#22D3EE"
chol_color = "#EF4444" if avg_chol > 240 else "#22D3EE"

# ================= KPI ROW =================
st.markdown("## 📊 Health Overview")
st.markdown("")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    metric_card("Population",
                f"{len(df):,}",
                "#22D3EE")

with col2:
    metric_card("Avg BMI",
                f"{avg_bmi:.2f}",
                bmi_color)

with col3:
    metric_card("Avg Sugar Intake",
                f"{df['sugar_intake'].mean():.2f}",
                "#A78BFA")

with col4:
    metric_card("Avg Disease Risk %",
                f"{avg_risk:.2f}%",
                risk_color)

with col5:
    metric_card("Avg Cholesterol",
                f"{avg_chol:.2f}",
                chol_color)

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