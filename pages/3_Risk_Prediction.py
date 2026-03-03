import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils.model_loader import load_model

st.set_page_config(layout="wide")

st.title("🤖 AI Disease Risk Prediction")

model, scaler = load_model()

# ================= LAYOUT =================
col1, col2 = st.columns([1, 1.2])

# ================= INPUT PANEL =================
with col1:
    st.markdown("### 📝 Enter Health Parameters")

    age = st.number_input("Age", 1, 100)
    bmi = st.number_input("BMI", 10.0, 50.0)
    daily_steps = st.number_input("Daily Steps", 0, 30000)
    stress_level = st.number_input("Stress Level (1-10)", 1, 10)
    sleep_hours = st.number_input("Sleep Hours", 0.0, 12.0)
    physical_activity = st.number_input("Physical Activity (minutes)", 0, 300)
    cholesterol = st.number_input("Cholesterol Level", 100, 400)
    glucose = st.number_input("Glucose Level", 50, 300)
    heart_rate = st.number_input("Heart Rate", 40, 150)

    predict_btn = st.button("🚀 Predict Risk")

# ================= PREDICTION PANEL =================
with col2:
    st.markdown("### 🧠 AI Risk Assessment")

    if predict_btn:

        input_data = np.array([[age, bmi, daily_steps, stress_level,
                                sleep_hours, physical_activity,
                                cholesterol, glucose, heart_rate]])

        scaled_data = scaler.transform(input_data)

        prediction = model.predict(scaled_data)[0]
        probability = model.predict_proba(scaled_data)[0][1] * 100

        # Dynamic Color
        if probability > 60:
            color = "#EF4444"
        elif probability > 35:
            color = "#F59E0B"
        else:
            color = "#10B981"

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=probability,
            number={'suffix': "%"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 35], 'color': "#064E3B"},
                    {'range': [35, 60], 'color': "#78350F"},
                    {'range': [60, 100], 'color': "#7F1D1D"},
                ],
            }
        ))

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            font={'color': "white"},
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        # Final Message
        if prediction == 1:
            st.error("⚠ High Disease Risk Detected")
        else:
            st.success("✅ Low Disease Risk Detected")

    else:
        st.info("Enter values and click Predict to see AI assessment.")