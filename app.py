import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib

# Load the model and scaler
model = joblib.load('logistic_model.pkl')
scaler = joblib.load('scaler.pkl')

st.title("Risk Prediction Application")

# Input fields
age = st.slider("Current Age", 18, 100, 30)
income = st.number_input("Yearly Income", min_value=0, value=50000)
debt = st.number_input("Total Debt", min_value=0, value=20000)
credit_score = st.slider("Credit Score", 300, 850, 700)
per_capita_income = st.number_input("Per Capita Income", min_value=0, value=20000)
gender = st.radio("Gender", ("Male", "Female"))

# Button to predict
if st.button("Predict Risk"):
    gender_values = [1, 0] if gender == "Male" else [0, 1]
    input_data = [[age, income, debt, credit_score, per_capita_income] + gender_values]
    scaled_data = scaler.transform(input_data)
    prediction = model.predict(scaled_data)[0]
    risk_category = ["Low Risk", "Medium Risk", "High Risk"][prediction]
    st.success(f"The predicted risk category is: {risk_category}")
