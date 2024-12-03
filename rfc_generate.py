import os
from google.cloud import  bigquery
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
# Replace with the actual path to your JSON key file
credentials_path = "/content/caixa-bank-6c4f815e89ac.json"


# Check if the file exists
if not os.path.exists(credentials_path):
    raise FileNotFoundError(f"Credentials file not found: {credentials_path}")

# Set the environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path


# This ensures that the changes are picked up by the BigQuery client library.
client = bigquery.Client()


            #### Getting Data from Big querry & transforming 

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


#### Creating Target value

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


#### target & features 

# Define features and target
X = aggregated_df[[
      'current_age',
      'yearly_income',
      'total_debt',
      'credit_score',
      'per_capita_income',
      'gender',
      #'amount', #with 0.98 #w/o 0.715
      'num_credit_cards',
      'retirement_age',
      'debt_to_income_ratio',
      'credit_utilization',
      'age_to_retirement_ratio',
      'debt_credit_interaction'
  ]]

y = aggregated_df['risk_category']

#### MODEL

#creating ML instance
clf = DecisionTreeClassifier()

# Train the model
clf.fit(X_train, y_train)

#### Make predictions Not 
#y_pred = clf.predict(X_test)

# Evaluate the model
#print("Accuracy:", accuracy_score(y_test, y_pred))
#print(classification_report(y_test, y_pred))
