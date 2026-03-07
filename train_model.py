import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

print("Starting model training...")

# ================= LOAD DATA =================
df = pd.read_csv("data/full_health_dataset.csv")

data = df.copy()

# ================= DATA CLEANING =================

num_col = [
    "blood_pressure","heart_rate","insulin",
    "daily_steps","income","daily_supplement_dosage",
    "stress_level","screen_time"
]

for col in num_col:
    data[col].fillna(data[col].median(), inplace=True)

cat_col = ["alcohol_consumption","exercise_type","caffeine_intake"]

for col in cat_col:
    data[col].fillna("Unknown", inplace=True)

# Drop unnecessary columns
data.drop(columns=["electrolyte_level"], inplace=True, errors="ignore")
data.drop(columns=["environmental_risk_score"], inplace=True, errors="ignore")
data.drop(columns=["bmi_estimated","bmi_scaled","bmi_corrected"], inplace=True, errors="ignore")
data.drop(columns=["survey_code"], inplace=True, errors="ignore")

# ================= FEATURE ENGINEERING =================

data["age_group"] = pd.cut(
    data["age"],
    bins=[0,25,40,60,100],
    labels=["Young","Adult","Middle","Senior"]
)

data["bmi_category"] = pd.cut(
    data["bmi"],
    bins=[0,18.5,25,30,100],
    labels=["Underweight","Normal","Overweight","Obese"]
)

data["activity_level"] = pd.cut(
    data["daily_steps"],
    bins=[0,5000,7500,20000],
    labels=["Sedentary","Moderate","Active"]
)

data["stress_category"] = pd.cut(
    data["stress_level"],
    bins=[0,3,6,10],
    labels=["Low","Moderate","High"],
    include_lowest=True
)
data["smoking_level"] = data["smoking_level"].map({
    "Non-smoker": 0,
    "Light": 1,
    "Heavy": 2
})
# ================= RISK SCORE =================

data["risk_score"] = 0

data.loc[data["bmi"] > 30, "risk_score"] += 1
data.loc[data["daily_steps"] < 4000, "risk_score"] += 1
data.loc[data["stress_level"] > 7, "risk_score"] += 1
data.loc[data["sleep_hours"] < 6, "risk_score"] += 1
data.loc[data["smoking_level"] == "Heavy", "risk_score"] += 1
data.loc[data["alcohol_consumption"] == "Regularly", "risk_score"] += 1
data.loc[data["physical_activity"] < 2, "risk_score"] += 1

# ================= TARGET VARIABLE =================

data["derived_target"] = data["risk_score"].apply(
    lambda x: 1 if x >= 3 else 0
)

# ================= MODEL FEATURES =================

features = [
    "age",
    "bmi",
    "daily_steps",
    "stress_level",
    "sleep_hours",
    "physical_activity",
    "cholesterol",
    "glucose",
    "heart_rate"
]

X = data[features]
y = data["derived_target"]

# ================= TRAIN TEST SPLIT =================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ================= SCALING =================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ================= MODEL TRAINING =================

rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

rf.fit(X_train_scaled, y_train)

# ================= EVALUATION =================

y_pred = rf.predict(X_test_scaled)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# ================= TRAIN FINAL MODEL =================

rf_full = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

rf_full.fit(X, y)

# ================= SAVE MODEL =================

joblib.dump(rf_full, "disease_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("Model saved successfully!")

# ================= SAVE DATA FOR DASHBOARD =================

data["model_prediction"] = rf_full.predict(X)
data["risk_probability"] = rf_full.predict_proba(X)[:,1]

data["model_prediction"] = data["model_prediction"].map({
    0:"Healthy",
    1:"Diseased"
})

data.to_csv("data/full_health_dataset.csv", index=False)

print("Training pipeline completed!")