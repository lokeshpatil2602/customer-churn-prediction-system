import pandas as pd

def preprocess_input(data):
    """
    Convert input data to DataFrame for prediction (preserves feature names).
    Args: data (dict) - dictionary with age, tenure, monthly_charges
    Returns: pd.DataFrame with shape (1, 3)
    """
    return pd.DataFrame([{
        'age': data['age'],
        'tenure': data['tenure'],
        'monthly_charges': data['monthly_charges']
    }])
