import streamlit as st
import numpy as np
from utils.model_loader import load_model

st.title("🤖 Disease Risk Prediction")

model, scaler = load_model()

age = st.number_input("Age", 1, 100)
bmi = st.number_input("BMI", 10.0, 50.0)
daily_steps = st.number_input("Daily Steps", 0, 30000)
stress_level = st.number_input("Stress Level (1-10)", 1, 10)
sleep_hours = st.number_input("Sleep Hours", 0.0, 12.0)
physical_activity = st.number_input("Physical Activity (minutes)", 0, 300)
cholesterol = st.number_input("Cholesterol Level", 100, 400)
glucose = st.number_input("Glucose Level", 50, 300)
heart_rate = st.number_input("Heart Rate", 40, 150)

if st.button("Predict Risk"):

    input_data = np.array([[age, bmi, daily_steps, stress_level,
                            sleep_hours, physical_activity,
                            cholesterol, glucose, heart_rate]])

    scaled_data = scaler.transform(input_data)

    prediction = model.predict(scaled_data)[0]
    probability = model.predict_proba(scaled_data)[0][1]

    if prediction == 1:
        st.error(f"⚠ High Disease Risk ({round(probability*100,2)}%)")
    else:
        st.success(f"✅ Low Disease Risk ({round(probability*100,2)}%)")