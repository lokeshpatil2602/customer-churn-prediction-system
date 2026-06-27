# Customer Churn Prediction System

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit)](https://customer-churn-prediction-system-zzrjybcqzpeisadtys6ydt.streamlit.app)
[![Backend API](https://img.shields.io/badge/Backend%20API-Railway-8B5CF6?logo=railway)](https://customer-churn-backend-production.up.railway.app)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/lokeshpatil2602/customer-churn-prediction-system)

An intermediate-level machine learning project that predicts customer churn using two popular algorithms — deployed live with a Flask REST API backend and Streamlit frontend.

---

## 🚀 Live Demo

| Service | URL |
|---------|-----|
| **Frontend (Streamlit)** | https://customer-churn-prediction-system-zzrjybcqzpeisadtys6ydt.streamlit.app |
| **Backend API (Flask)** | https://customer-churn-backend-production.up.railway.app |

### API Quick Test
```bash
# Health check
curl https://customer-churn-backend-production.up.railway.app/

# Model accuracy
curl https://customer-churn-backend-production.up.railway.app/accuracy

# Predict churn
curl -X POST https://customer-churn-backend-production.up.railway.app/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 25, "tenure": 3, "monthly_charges": 85.0}'
```

---

## What is Customer Churn Prediction?

Customer churn prediction helps businesses identify customers who are likely to stop using their services. By predicting churn, companies can:
- Take action to retain valuable customers
- Improve customer satisfaction
- Reduce revenue loss

---

## Technology Stack

**Backend:**
- Flask (Python web framework)
- Scikit-learn (Machine Learning)
- Pandas (Data processing)
- Gunicorn (Production WSGI server)
- Deployed on **Railway**

**Frontend:**
- Streamlit (Web interface)
- Deployed on **Streamlit Community Cloud**

**Machine Learning Models:**
- Logistic Regression
- Decision Tree

---

## Project Structure

```
customer-churn-prediction-system/
│
├── backend/
│   ├── app.py              # Flask API server
│   ├── model.py            # Model training script
│   ├── utils.py            # Helper functions
│   ├── lr.pkl              # Logistic Regression model
│   ├── dt.pkl              # Decision Tree model
│   ├── accuracy.pkl        # Model accuracy scores
│   ├── requirements.txt    # Backend dependencies
│   ├── Procfile            # Deployment entrypoint
│   ├── railway.toml        # Railway config
│   └── test_backend.py     # Test suite (33 tests)
│
├── frontend/
│   ├── app.py              # Streamlit web interface
│   ├── config.py           # Backend URL config
│   ├── requirements.txt    # Frontend dependencies
│   ├── .streamlit/
│   │   └── config.toml     # Streamlit theme config
│   ├── static/
│   │   └── style.css       # Custom styling
│   └── components/
│       ├── dashboard.py    # Dashboard page
│       ├── predict.py      # Prediction page
│       ├── train.py        # Model training page
│       └── history.py      # Prediction history page
│
├── dataset/
│   └── churn.csv           # Customer data
│
├── docker-compose.yml      # Run both services with Docker
├── render.yaml             # Render deployment config
└── README.md
```

---

## Features

### Dashboard
- Live model accuracy metrics from the API
- Churn vs Stay prediction bar charts
- Model agreement analysis
- Auto-updates with new predictions

### Predict
- Enter customer details (age, tenure, monthly charges + 14 more fields)
- Get predictions from both Logistic Regression and Decision Tree
- Visual probability chart
- Results saved to session history

### Train Models
- Upload your own CSV dataset
- Retrain models with new data
- Compare model accuracies
- Active model auto-selected based on best accuracy

### History
- View all past predictions in a table
- Summary statistics (total, churn, stay counts)
- Clear history option

---

## Machine Learning Models

### Logistic Regression
- **Type**: Statistical classification algorithm
- **Advantage**: Provides probability scores, easy to interpret

### Decision Tree
- **Type**: Tree-based classification algorithm
- **Advantage**: Handles complex patterns, easy to visualize

---

## API Endpoints

### `GET /`
Returns welcome message.

### `GET /accuracy`
```json
{
  "logistic_regression": "1.00",
  "decision_tree": "1.00"
}
```

### `POST /predict`
**Request:**
```json
{
  "age": 30,
  "tenure": 12,
  "monthly_charges": 50.0
}
```
**Response:**
```json
{
  "lr_prediction": 0,
  "dt_prediction": 1,
  "probability": [0.70, 0.30]
}
```

---

## Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/lokeshpatil2602/customer-churn-prediction-system.git
cd customer-churn-prediction-system
```

### 2. Install dependencies
```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 3. Train models
```bash
cd backend
python model.py
```

### 4. Start backend
```bash
cd backend
python app.py
# Flask API running at http://localhost:5000
```

### 5. Start frontend (new terminal)
```bash
cd frontend
streamlit run app.py
# Streamlit app at http://localhost:8501
```

### Run with Docker
```bash
docker-compose up --build
```

---

## Run Tests
```bash
cd backend
python test_backend.py
```
33 tests covering utils, model files, ML predictions, and all API endpoints.

---

## Deployment

| Service | Platform | URL |
|---------|----------|-----|
| Backend (Flask API) | Railway | https://customer-churn-backend-production.up.railway.app |
| Frontend (Streamlit) | Streamlit Cloud | https://customer-churn-prediction-system-zzrjybcqzpeisadtys6ydt.streamlit.app |

The frontend reads `BACKEND_URL` from environment variables / Streamlit secrets, so it works both locally and in production without code changes.

---

## Dataset Features

| Feature | Description |
|---------|-------------|
| `age` | Customer age (18–100) |
| `tenure` | Months with company |
| `monthly_charges` | Monthly bill amount ($) |
| `churn` | Target: Yes / No |

---

**Built with Python, Flask, Streamlit, and Machine Learning**
