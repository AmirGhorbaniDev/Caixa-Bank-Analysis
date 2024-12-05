import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the trained RandomForest model
model_path = 'put your link'  # Path to the saved model
model = joblib.load(model_path)  # Load the RandomForestClassifier

# Feature names (based on your training data)
feature_names = [
    'current_age',
    'yearly_income',
    'total_debt',
    'credit_score',
    'per_capita_income',
    'gender',
    'amount',
    'num_credit_cards',
    'retirement_age',
    'debt_to_income_ratio',
    'credit_utilization',
    'age_to_retirement_ratio',
    'debt_credit_interaction'
]

# Get feature importances
importances = model.feature_importances_

# Create a DataFrame for better readability
feature_importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

# Print feature importance
print(feature_importance_df)

# Plot feature importance
plt.figure(figsize=(12, 6))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'], color='skyblue')
plt.xlabel('Importance Score')
plt.ylabel('Features')
plt.title('Feature Importance Analysis (Random Forest)')
plt.gca().invert_yaxis()  # Most important feature on top
plt.tight_layout()
plt.show()
