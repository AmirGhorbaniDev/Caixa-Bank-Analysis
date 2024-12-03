import streamlit as st
import joblib
import numpy as np
from PIL import Image

# Load the trained model and 
model_path = "/Users/amir/Desktop/Caixa Bank/Caixa-Bank-Analysis/rfc.pkl"  # Update with your model path

model = joblib.load(model_path)


# Custom CSS for styling
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
    .accepted-box {
        background-color: #d4edda;
        color: #155724;
        padding: 20px;
        border: 2px solid #c3e6cb;
        border-radius: 5px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
    }
    .rejected-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 20px;
        border: 2px solid #f5c6cb;
        border-radius: 5px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
    }
    footer {visibility: hidden;} /* Hide footer */
    .viewerBadge_container__1QSob {visibility: hidden;} /* Hide Streamlit badge */
    </style>
    """,
    unsafe_allow_html=True
)

# App Header and Description
st.title("🌟 Risk Prediction Model")
st.header("Predict Customer Risk Category")
st.write(
    """
    Enter the customer details below and get the prediction in real-time. This tool predicts if a customer is **Accepted** or **Rejected**.
    """
)

# Add a logo image
image = Image.open('/Users/amir/Desktop/Caixa Bank/CaixaBank_logo.svg.png')  # Update with your image path
st.image(image, caption="Risk Prediction Analysis", use_column_width=True)

# Input fields for customer details
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
debt_to_income_ratio = total_debt / yearly_income if yearly_income > 0 else 0
credit_utilization = st.number_input("Credit Utilization", value=0.5)
age_to_retirement_ratio = (retirement_age - current_age) / retirement_age if retirement_age > 0 else 0
debt_credit_interaction = st.number_input("Debt-Credit Interaction", value=10000.0)

# Button for Prediction
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


    # Predict the risk category
    prediction = model.predict(input_data)[0]

    # Display results with styling
    if prediction == 0:
        st.markdown('<div class="accepted-box">Accepted</div>', unsafe_allow_html=True)
    elif prediction == 1:
        st.markdown('<div class="rejected-box">Rejected</div>', unsafe_allow_html=True)
