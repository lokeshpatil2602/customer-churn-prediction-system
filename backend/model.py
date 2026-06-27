import pandas as pd  
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

# Load dataset from CSV
df = pd.read_csv('../dataset/churn.csv')

# Convert churn from Yes/No to 1/0
df['churn'] = df['churn'].map({'Yes': 1, 'No': 0})

# Prepare features (X) and target (y)
X = df[['age', 'tenure', 'monthly_charges']]
y = df['churn']

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Logistic Regression model
lr_model = LogisticRegression(random_state=42)
lr_model.fit(X_train, y_train)

# Train Decision Tree model
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)

# Calculate accuracy for both models
lr_pred = lr_model.predict(X_test)
dt_pred = dt_model.predict(X_test)

lr_accuracy = accuracy_score(y_test, lr_pred)
dt_accuracy = accuracy_score(y_test, dt_pred)

# Save trained models using pickle
pickle.dump(lr_model, open('lr.pkl', 'wb'))
pickle.dump(dt_model, open('dt.pkl', 'wb'))

# Save accuracy scores to a file for frontend use
accuracy_data = {
    'lr_accuracy': lr_accuracy,
    'dt_accuracy': dt_accuracy
}
pickle.dump(accuracy_data, open('accuracy.pkl', 'wb')) # store object in file

print(f"Models trained successfully!")
print(f"Logistic Regression Accuracy: {lr_accuracy:.2f}")
print(f"Decision Tree Accuracy: {dt_accuracy:.2f}")
