# Customer Churn Prediction System

An intermediate-level machine learning project that predicts customer churn using two popular algorithms.

## What is Customer Churn Prediction?

Customer churn prediction helps businesses identify customers who are likely to stop using their services. By predicting churn, companies can:
- Take action to retain valuable customers
- Improve customer satisfaction
- Reduce revenue loss

## Technology Stack

**Backend:**
- Flask (Python web framework)
- Scikit-learn (Machine Learning)
- Pandas (Data processing)

**Frontend:**
- Streamlit (Web interface)

**Machine Learning Models:**
- Logistic Regression
- Decision Tree

## Project Structure

```
customer-churn/
|
|-- backend/
|   |-- app.py              # Flask API server
|   |-- model.py            # Model training script
|   |-- utils.py            # Helper functions
|   |-- lr.pkl              # Logistic Regression model
|   |-- dt.pkl              # Decision Tree model
|   |-- accuracy.pkl        # Model accuracy scores
|
|-- frontend/
|   |-- app.py              # Streamlit web interface
|
|-- dataset/
|   |-- churn.csv           # Customer data
|
`-- README.md               # This file
```

## Features

### Backend (Flask API)
- **Model Training**: Trains both Logistic Regression and Decision Tree
- **Accuracy Calculation**: Shows model performance on test data
- **REST API**: Provides prediction endpoints
- **Helper Functions**: Simple data preprocessing

### Frontend (Streamlit)
- **User Interface**: Clean and intuitive web form
- **Real-time Predictions**: Instant results from both models
- **Accuracy Display**: Shows model performance metrics
- **Probability Charts**: Visual representation of churn probability

## Machine Learning Models

### Logistic Regression
- **Type**: Statistical classification algorithm
- **How it works**: Predicts probability of churn using mathematical equation
- **Advantage**: Provides probability scores, easy to interpret

### Decision Tree
- **Type**: Tree-based classification algorithm
- **How it works**: Makes decisions by asking questions about customer features
- **Advantage**: Handles complex patterns, easy to visualize

## How to Run the Project

### Step 1: Install Dependencies
```bash
pip install flask streamlit scikit-learn pandas requests
```

### Step 2: Train Models
```bash
cd backend
python model.py
```
This will:
- Load the dataset
- Train both models
- Calculate accuracy
- Save models as .pkl files

### Step 3: Start Backend Server
```bash
cd backend
python app.py
```
The Flask API will start on http://localhost:5000

### Step 4: Start Frontend
```bash
cd frontend
streamlit run app.py
```
The Streamlit app will open in your browser

## API Endpoints

### GET `/`
Returns welcome message

### GET `/accuracy`
Returns model accuracy scores:
```json
{
  "logistic_regression": "0.85",
  "decision_tree": "0.90"
}
```

### POST `/predict`
Accepts customer data and returns predictions:
```json
Request: {
  "age": 30,
  "tenure": 12,
  "monthly_charges": 50.0
}

Response: {
  "lr_prediction": 0,
  "dt_prediction": 1,
  "probability": [0.7, 0.3]
}
```

## Dataset Features

The system uses three customer features:
- **age**: Customer age (18-100)
- **tenure**: How long customer has been with company (months)
- **monthly_charges**: Monthly bill amount ($)

**Target**: churn (0 = Stay, 1 = Churn)

## Sample Usage

1. Open the Streamlit app in your browser
2. Enter customer information:
   - Age: 35
   - Tenure: 18 months
   - Monthly Charges: $60
3. Click "Predict"
4. View results:
   - Model predictions (Stay/Churn)
   - Probability percentages
   - Performance metrics

## Model Performance

The system shows accuracy for both models:
- **Logistic Regression**: Typically 80-90% accuracy
- **Decision Tree**: Typically 85-95% accuracy

Accuracy is calculated on test data (20% of dataset) to ensure realistic performance.

## Why This Project?

### Educational Value
- **Simple Code**: Easy to understand and modify
- **Clear Structure**: Organized backend/frontend separation
- **Real Application**: Practical business problem
- **Multiple Models**: Compare different algorithms

### Technical Skills
- Machine Learning model training
- REST API development
- Web interface creation
- Data preprocessing
- Model evaluation

## Future Improvements

- Add more customer features
- Include more ML models
- Add data visualization
- Implement model tuning
- Add customer segmentation

## Troubleshooting

**Backend not connecting**: Make sure Flask server is running on port 5000

**Models not found**: Run `python model.py` first to train and save models

**Accuracy not showing**: Check if accuracy.pkl file exists in backend folder

**Frontend errors**: Ensure all dependencies are installed

---

**Built with Python, Flask, Streamlit, and Machine Learning**
