# 🛡️ Fraud Risk Analysis Project

🚀 **Analyze customer data to assess risk levels with precision and clarity.** This project utilizes cutting-edge tools and advanced data analytics to classify customers into risk categories—**High Risk**, **Medium Risk**, and **Low Risk**—based on financial and behavioral metrics such as income, debt, credit scores, and fraud history.

---

## 📖 Overview
This project leverages **SQL** and **Google BigQuery** to:
1. 🧹 **Clean and transform data**: Preparing fields for accurate analysis.
2. 📊 **Calculate risk categories**: Introducing a `risk_category` column with custom logic.
3. 🔍 **Enhance dataset**: Adding a `has_fraud_history` column for easy fraud detection.
4. 🏁 **Deliver a final enriched table**: Ready for visualization, reporting, or further analysis.

---

## 📂 Dataset

### Fields:
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
| `has_fraud_history` | INTEGER  | Indicates fraud history (1 for yes, 0 for no)      |
| `risk_category`     | STRING   | Categorized risk level of the customer             |

---

## ⚙️ Risk Categorization Logic

The `risk_category` is calculated using this custom logic:
- **High Risk**:
  - Fraud count > 20
  - Credit score < 600 **AND** total debt > 50,000
- **Medium Risk**:
  - Fraud count between 1 and 20
  - Credit score between 600 and 750 **AND** total debt between 20,000 and 50,000
- **Low Risk**:
  - Fraud count = 0 **AND** credit score >= 750
  - Default: Low Risk if no other conditions match

---

## 🛠️ Steps to Reproduce

### 1️⃣ Data Cleaning
1. Import raw data into BigQuery.
2. Validate data types (`INTEGER`, `STRING`, etc.) and handle duplicates or null values.

### 2️⃣ Add `risk_category` Column
Use this SQL query to classify customers into risk levels:
```sql
CREATE OR REPLACE TABLE `project.dataset.generateddata_with_risk` AS
SELECT
    *,
    CASE
        WHEN fraud_count > 20 THEN 'High Risk'
        WHEN credit_score < 600 AND total_debt > 50000 THEN 'High Risk'
        WHEN fraud_count BETWEEN 1 AND 20 THEN 'Medium Risk'
        WHEN credit_score BETWEEN 600 AND 750 AND total_debt BETWEEN 20000 AND 50000 THEN 'Medium Risk'
        WHEN fraud_count = 0 AND credit_score >= 750 THEN 'Low Risk'
        ELSE 'Low Risk'
    END AS risk_category
FROM
    `project.dataset.generateddata`;

### 3️⃣ Add has_fraud_history Column
This column flags customers with a fraud history:

sql
Copy code
CREATE OR REPLACE TABLE `project.dataset.generateddata_with_fraud_history` AS
SELECT
    *,
    CASE 
        WHEN fraud_count > 0 THEN 1
        ELSE 0
    END AS has_fraud_history
FROM
    `project.dataset.generateddata_with_risk`;
### 4️⃣ Publish Final Table
Export the final enriched table with all new columns for visualization or reporting.

### 🛠️ Tools & Technologies
Google BigQuery: SQL-based data analysis and transformation.
Python: For machine learning integration and data preprocessing.
GitHub: To track changes and document the project.
🗂️ File Structure
plaintext
Copy code
.
├── 📁 Database/               # Dataset storage and updates
├── 📁 app/                    # Code and scripts for transformations
├── README.md                  # Documentation
├── clf.pkl                    # Machine Learning model file
├── Dashboard.png              # Sample visualization
├── SQL_Scripts/               # SQL queries used for data processing
└── Outputs/                   # Final results and reports
### 📊 Visualization

### 🚀 How to Run
Clone this repository:

git clone https://github.com/AmirGhorbaniDev/fraud-risk-analysis.git
Navigate to the project directory:

cd fraud-risk-analysis
Open and execute SQL scripts in BigQuery.
Analyze and visualize the results using your preferred BI tool.
---
### 🤝 Contributions
We welcome contributions! Feel free to:

Open an issue.
Submit a pull request.
Share your feedback to improve the project.
📜 License
This project is licensed under the MIT License. See the LICENSE file for details.
---
### 🙋‍♂️ Author
👤 Amir Ghorbani

✨ Special thanks to the amazing contributors:

Kai
Donald
🛠️ Dataset Source
Kaggle: Transactions Fraud Datasets
---
🚀 Let’s make data analysis powerful and accessible!
Feel free to fork and start exploring the world of fraud detection.


--- 
This README includes a professional yet stylish structure with emojis, Markdown styling, and clear sections for easy navigation.





