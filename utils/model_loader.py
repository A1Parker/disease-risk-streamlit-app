import joblib

def load_model():
    model = joblib.load("disease_model.pkl")
    scaler = joblib.load("scaler.pkl")
    return model, scaler