import streamlit as st
import joblib
import numpy as np
from PIL import Image

# Load the model and scaler
model_path = ''  # Replace with the path to your uploaded model
scaler_path = ''  # Replace with the path to your scaler, if any

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Add custom styling with blue theme
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }
    .stTextInput, .stNumberInput, .stSelectbox {
        border: 2px solid #007BFF;
        border-radius: 5px;
        padding: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add app header and description
st.title("🌟 Risk Prediction Model")
st.header("Predict Customer Risk Category")
st.write(
    """
    Enter the details below to predict the customer's risk category. 
    This model evaluates factors like income, credit score, and debt-to-income ratio to provide risk insights.
    """
)

# Add an image for visual enhancement
image = Image.open('/Users/amir/Desktop/Caixa Bank/CaixaBank_logo.svg.png')  # Replace with your image path
st.image(image, caption="Risk Prediction Analysis", use_column_width=True)

# Organize input fields into tabs
tab1, tab2 = st.tabs(["Input Data", "Prediction Result"])

with tab1:
    st.subheader("Enter Customer Details")
    
    col1, col2 = st.columns(2)

    with col1:
        current_age = st.number_input("Current Age", min_value=18, max_value=100, value=30)
        yearly_income = st.number_input("Yearly Income", value=50000.0)
        total_debt = st.number_input("Total Debt", value=20000.0)
        credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=700)

    with col2:
        per_capita_income = st.number_input("Per Capita Income", value=20000.0)
        gender = st.selectbox("Gender", options=["Male", "Female"])
        amount = st.number_input("Total Amount", value=20000.0)
        num_credit_cards = st.number_input("Number of Credit Cards", min_value=0, value=3)

    retirement_age = st.number_input(
        "Retirement Age", 
        min_value=current_age + 1, 
        value=max(65, current_age + 1)
    )
    debt_to_income_ratio = total_debt / yearly_income
    credit_utilization = st.number_input("Credit Utilization", value=0.5)
    age_to_retirement_ratio = (retirement_age - current_age) / retirement_age
    debt_credit_interaction = st.number_input("Debt-Credit Interaction", value=10000.0)

    # Display the input data for verification
    input_data_dict = {
        "Current Age": current_age,
        "Yearly Income": yearly_income,
        "Total Debt": total_debt,
        "Credit Score": credit_score,
        "Per Capita Income": per_capita_income,
        "Gender": gender,
        "Amount": amount,
        "Number of Credit Cards": num_credit_cards,
        "Retirement Age": retirement_age,
        "Debt-to-Income Ratio": debt_to_income_ratio,
        "Credit Utilization": credit_utilization,
        "Age-to-Retirement Ratio": age_to_retirement_ratio,
        "Debt-Credit Interaction": debt_credit_interaction
    }
    st.json(input_data_dict)

with tab2:
    st.subheader("Prediction Result")
    if st.button("Predict Risk"):
        # Prepare the input array
        gender_value = 0 if gender == "Male" else 1
        input_data = np.array([[
            current_age,
            yearly_income,
            total_debt,
            credit_score,
            per_capita_income,
            gender_value,
            amount,
            num_credit_cards,
            retirement_age,
            debt_to_income_ratio,
            credit_utilization,
            age_to_retirement_ratio,
            debt_credit_interaction
        ]])

        # Scale the input data
        scaled_data = scaler.transform(input_data)

        # Predict the risk category
        prediction = model.predict(scaled_data)[0]

        # Display the result
        st.success(f"The predicted risk category is: {prediction}")
