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
        ## recommendation code
        st.markdown("### 🩺 Personalized Health Insights")

recommendations = []

# --- High Risk Logic ---
if probability > 50:

    if physical_activity < 30:
        recommendations.append("• Increase daily physical activity to at least 30 minutes.")

    if sleep_hours < 6:
        recommendations.append("• Improve sleep duration (target 7–8 hours per night).")

    if stress_level > 7:
        recommendations.append("• Practice stress management techniques (meditation, breathing exercises).")

    if daily_steps < 5000:
        recommendations.append("• Increase daily steps (aim for 8,000–10,000 steps).")

    if cholesterol > 240:
        recommendations.append("• Monitor cholesterol levels and consider dietary adjustments.")

    if glucose > 140:
        recommendations.append("• Monitor glucose levels and reduce sugar intake.")

    if heart_rate > 100:
        recommendations.append("• Elevated heart rate detected — consider cardiovascular evaluation.")

    if recommendations:
        for rec in recommendations:
            st.warning(rec)
    else:
        st.warning("General lifestyle improvement recommended. Consider consulting a healthcare professional.")

# --- Low Risk Reinforcement ---
elif probability < 25:

    positive_points = []

    if physical_activity >= 30:
        positive_points.append("✔ Good physical activity level.")

    if sleep_hours >= 7:
        positive_points.append("✔ Healthy sleep duration.")

    if stress_level <= 5:
        positive_points.append("✔ Well-managed stress levels.")

    if daily_steps >= 7000:
        positive_points.append("✔ Active daily movement.")

    if cholesterol < 200:
        positive_points.append("✔ Healthy cholesterol range.")

    if glucose < 110:
        positive_points.append("✔ Stable glucose level.")

    if positive_points:
        st.success("🎉 You are maintaining good health habits!")
        for point in positive_points:
            st.success(point)
    else:
        st.success("You are currently at low risk. Maintain a balanced lifestyle to stay healthy.")

# --- Moderate Risk ---
else:
    st.info("⚠ Moderate risk detected. Small lifestyle improvements can significantly reduce future risk.")

#else:
    #st.info("Enter values and click Predict to see AI assessment.")