# -*- coding: utf-8 -*-
"""clf_Risk_model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IGL3iahJaKYwnkAFJs14l0m-ADGeg6IC
"""

#pip install pycaret

import os
from google.cloud import  bigquery
import pandas as pd

# Replace with the actual path to your JSON key file
credentials_path = "/Users/amir/Downloads/caixa-bank-6c4f815e89ac.json"

# Check if the file exists
if not os.path.exists(credentials_path):
    raise FileNotFoundError(f"Credentials file not found: {credentials_path}")

# Set the environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# **Important**: Restart the kernel or runtime environment after setting the environment variable.
# This ensures that the changes are picked up by the BigQuery client library.
client = bigquery.Client()

# getting client data
query = """ SELECT * FROM `caixa-bank.ML.risk_table`"""
risk_df = client.query(query).to_dataframe()

# getting transaction data
query = """ SELECT * FROM `caixa-bank.MAIN.transa_fraud_mcc`"""
transaction_df = client.query(query).to_dataframe()

#formatting and joining
risk_df.rename(columns={'customer_id':'client_id'}, inplace=True)
df_data= pd.merge(risk_df, transaction_df, how='left', on='client_id')


#removing unused colums
df_data.pop('fraud_count')
df_data.pop('mcc')
df_data.pop('id')
df_data.pop('date')
df_data.pop('use_chip')
df_data.pop('zip')
df_data.pop('online')
df_data.pop('merchant')
df_data.pop('merchant_id')
df_data.pop('merchant_city')
df_data.pop('merchant_state')
df_data.pop('card_id')

# value formating
df_data['fraud'] = df_data['fraud'].map({True: 1, False: 0})
df_data.replace({'gender':'Male'}, 0, inplace=True)
df_data.replace({'gender':'Female'}, 1, inplace=True)

# creating aggregated data frame
aggregated_df = df_data.groupby('client_id').agg({
    'current_age': 'max',
    'yearly_income': 'max',
    'total_debt': 'max',
    'credit_score': 'max',
    'per_capita_income': 'max',
    'fraud': 'sum',
    'gender': 'max',
    'amount': 'sum',
    'num_credit_cards': 'max',
    'retirement_age': 'max'
}).reset_index()

#adding calcuations
aggregated_df['debt_to_income_ratio']    =  aggregated_df['total_debt'] / aggregated_df['yearly_income'] # Customers with higher debt-to-income ratios are generally riskier.
aggregated_df['credit_utilization']      =  aggregated_df['total_debt'] / (aggregated_df['num_credit_cards'] * aggregated_df['credit_score'])# Customers with higher utilization (close to 1 or more) are generally riskier.
aggregated_df['age_to_retirement_ratio'] =  (aggregated_df['retirement_age'] - aggregated_df['current_age']) / aggregated_df['retirement_age']#Younger customers may behave differently than those nearing retirement.
aggregated_df['has_fraud_history']       =   aggregated_df['fraud'].apply(lambda x: 1 if x > 0 else 0)
aggregated_df['debt_credit_interaction'] =   aggregated_df['total_debt'] * aggregated_df['credit_score']

#creating risk function
def calculate_risk_category(row):
    if row['fraud'] > 0:
      return 1
    elif row['fraud'] == 0:
      return 0
    else :
      return 0

# adding risk collum
aggregated_df['risk_category'] = aggregated_df.apply(calculate_risk_category, axis=1).astype(int)

#priting aggregated_df to check for ML
aggregated_df.head()

aggregated_df.groupby('risk_category').mean()

aggregated_df['calc'] = (aggregated_df['yearly_income'] + aggregated_df['per_capita_income'] - aggregated_df['total_debt'])

aggregated_df.groupby('risk_category').nunique()
------------------------------------------------------------------------------------------------------
from sklearn.model_selection import train_test_split

# Define features and target
X = aggregated_df[[
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
  ]]

y = aggregated_df['risk_category']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

aggregated_df.head()

aggregated_df.pop('fraud')
aggregated_df.pop('has_fraud_history')
aggregated_df.pop('client_id')

from pycaret.classification import setup
xp = setup(
            data=X,
           target = y,
          normalize = True,
           session_id = 42)

from pycaret.classification import compare_models

best_model = compare_models()

from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

clf = XGBClassifier()

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.4f}')


print(classification_report(y_test, y_pred))

from sklearn.tree import DecisionTreeClassifier

clf = DecisionTreeClassifier(random_state=42)

# Train the model
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

from sklearn.ensemble import RandomForestClassifier

rfc = RandomForestClassifier()


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
rfc.fit(X_train, y_train)

# Make predictions
y_pred = rfc.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

import joblib

# Save the trained model
joblib.dump(rfc, 'rfc.pkl')

# Save the scaler
joblib.dump(scaler, 'rfc_scaler.pkl')

print("Model and scaler saved successfully!")

-------------------------------------------------------------------------------------
import pandas as pd

A = [{"Current Age":90,"Yearly Income":50000,"Total Debt":0,"Credit Score":400,"Per Capita Income":1000,"Gender":1,"Amount":200000000,"Number of Credit Cards":9,"Retirement Age":91,"Debt-to-Income Ratio":0,"Credit Utilization":0.5,"Age-to-Retirement Ratio":0.01098901098901099,"Debt-Credit Interaction":10000}]

# Convert the list of dictionaries to a pandas DataFrame
A_df = pd.DataFrame(A)

#Rename columns to match the training data
A_df = A_df.rename(columns={
    "Current Age": "current_age",
    "Yearly Income": "yearly_income",
    "Total Debt": "total_debt",
    "Credit Score": "credit_score",
    "Per Capita Income": "per_capita_income",
    "Gender": "gender",
    "Amount": "amount",
    "Number of Credit Cards": "num_credit_cards",
    "Retirement Age": "retirement_age",
    "Debt-to-Income Ratio": "debt_to_income_ratio",
    "Credit Utilization": "credit_utilization",
    "Age-to-Retirement Ratio": "age_to_retirement_ratio",
    "Debt-Credit Interaction": "debt_credit_interaction"
})


# Now you can use the DataFrame for prediction
predictions = rfc.predict(A_df)
print(predictions)

