# Fraud Risk Analysis Project

This project analyzes customer data to assess their risk levels based on financial and behavioral metrics. The data includes information such as income, debt, credit scores, and fraud history, and the project categorizes customers into different risk categories: High Risk, Medium Risk, and Low Risk.

## Project Overview
This project utilizes SQL and BigQuery to:
1. **Clean and transform data**: Ensure all data fields are ready for analysis.
2. **Calculate risk categories**: Add a calculated `risk_category` column based on predefined rules.
3. **Enhance dataset**: Introduce a new `has_fraud_history` column to indicate whether a customer has a history of fraud.
4. **Publish final dataset**: Create a clean, enriched table ready for further analysis or reporting.

## Dataset
The dataset includes the following fields:

| Column Name         | Type     | Description                                         |
|---------------------|----------|-----------------------------------------------------|
| `customer_id`       | INTEGER  | Unique identifier for each customer                |
| `current_age`       | INTEGER  | Current age of the customer                        |
| `yearly_income`     | INTEGER  | Yearly income of the customer                      |
| `total_debt`        | INTEGER  | Total debt of the customer                         |
| `credit_score`      | INTEGER  | Credit score of the customer                       |
| `per_capita_income` | INTEGER  | Per capita income                                  |
| `retirement_age`    | INTEGER  | Expected retirement age                            |
| `gender`            | STRING   | Gender of the customer                             |
| `num_credit_cards`  | INTEGER  | Number of credit cards owned                       |
| `fraud_count`       | INTEGER  | Number of fraud incidents                          |
| `has_fraud_history` | INTEGER  | Indicates if the customer has fraud history (1/0)  |
| `risk_category`     | STRING   | Categorized risk level of the customer             |

## Risk Category Logic
The `risk_category` is determined using the following logic:

- **High Risk**:
  - Fraud count > 20
  - Credit score < 600 AND total debt > 50,000
- **Medium Risk**:
  - Fraud count BETWEEN 1 AND 20
  - Credit score BETWEEN 600 AND 750 AND total debt BETWEEN 20,000 AND 50,000
- **Low Risk**:
  - Fraud count = 0 AND credit score >= 750
  - Default to "Low Risk" if no other condition matches

## Steps to Reproduce

### 1. Data Cleaning
- Import raw data into BigQuery.
- Ensure all fields are properly typed (e.g., `INTEGER`, `STRING`).
- Remove duplicates and handle null values if necessary.

### 2. Risk Category Calculation
Run the following query to add the `risk_category` column:
```sql
CREATE OR REPLACE TABLE `caixa-bank.ML.generateddata_with_risk` AS
SELECT
    customer_id,
    current_age,
    yearly_income,
    total_debt,
    credit_score,
    per_capita_income,
    retirement_age,
    gender,
    num_credit_cards,
    fraud_count,
    CASE
        WHEN fraud_count > 20 THEN 'High Risk'
        WHEN credit_score < 600 AND total_debt > 50000 THEN 'High Risk'
        WHEN fraud_count BETWEEN 1 AND 20 THEN 'Medium Risk'
        WHEN credit_score BETWEEN 600 AND 750 AND total_debt BETWEEN 20000 AND 50000 THEN 'Medium Risk'
        WHEN fraud_count = 0 AND credit_score >= 750 THEN 'Low Risk'
        ELSE 'Low Risk'
    END AS risk_category
FROM
    `caixa-bank.ML.generateddata`;
```

### 3. Add `has_fraud_history` Column
Run the following query to add the `has_fraud_history` column:
```sql
CREATE OR REPLACE TABLE `caixa-bank.ML.generateddata_with_fraud_history` AS
SELECT
    customer_id,
    current_age,
    yearly_income,
    total_debt,
    credit_score,
    per_capita_income,
    retirement_age,
    gender,
    num_credit_cards,
    fraud_count,
    CASE 
        WHEN fraud_count > 0 THEN 1
        ELSE 0
    END AS has_fraud_history,
    risk_category
FROM
    `caixa-bank.ML.generateddata_with_risk`;
```

### 4. Publish Final Table
The final table includes all columns with the new `has_fraud_history` and `risk_category` fields. Export this table for analysis or visualization.

## File Structure
```
.
├── README.md          # Project documentation
├── SQL Scripts        # Contains SQL queries for data processing
├── Data Samples       # Sample datasets (if applicable)
└── Outputs            # Final output tables or visualizations
```

## Tools and Technologies
- **Google BigQuery**: For SQL-based data transformation.
- **GitHub**: To publish and document the project.
- **SQL**: To clean, transform, and analyze data.

## Usage
1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/fraud-risk-analysis.git
    ```
2. Navigate to the project directory:
    ```bash
    cd fraud-risk-analysis
    ```
3. Review and execute SQL scripts in the `SQL Scripts` folder using BigQuery.

## Contributions
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author
[Your Name](https://github.com/your-username)

---
Feel free to reach out for questions or suggestions!
