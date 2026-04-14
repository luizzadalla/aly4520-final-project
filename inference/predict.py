import joblib
import pandas as pd

model = joblib.load("models/model.pkl")

sample = {
    "gender": 1,
    "height": 170,
    "weight": 70,
    "ap_hi": 120,
    "ap_lo": 80,
    "cholesterol": 1,
    "gluc": 1,
    "smoke": 0,
    "alco": 0,
    "active": 1,
    "age_years": 50
}

df = pd.DataFrame([sample])

pred = model.predict(df)

print("Prediction:", pred)