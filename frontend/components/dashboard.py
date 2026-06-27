import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import BACKEND_URL

def show_dashboard():
    """Display dashboard page with overview and statistics"""
    st.title("Dashboard")
    st.write("Overview of Customer Churn Prediction System")
    
    # ==================== MODEL PERFORMANCE SECTION ====================
    show_model_performance()
    
    # ==================== PREDICTION STATISTICS SECTION ====================
    show_prediction_statistics()
    
    
def show_model_performance():
    """Display model accuracy and performance metrics with persistence"""
    st.subheader("Model Performance")
    
    # Show active model information if available
    if st.session_state.get('active_model') and st.session_state.get('training_completed'):
        show_active_model_status()
    
    try:
        # Get model accuracy from backend API
        accuracy_response = requests.get(f"{BACKEND_URL}/accuracy")
        accuracy_data = accuracy_response.json()
        lr_acc = accuracy_data['logistic_regression']
        dt_acc = accuracy_data['decision_tree']
        
        # Display model performance cards
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Logistic Regression Accuracy", lr_acc)
        with col2:
            st.metric("Decision Tree Accuracy", dt_acc)
            
    except:
        st.warning("Could not fetch model accuracy. Make sure backend is running.")

def show_active_model_status():
    """Display active model status from session state"""
    active_model = st.session_state.get('active_model')
    active_accuracy = st.session_state.get('active_accuracy')
    
    if active_model and active_accuracy:
        st.success(f"**Active Model**: {active_model} (Accuracy: {active_accuracy:.2f})")
        st.info("This model was selected based on highest accuracy during training.")

def show_prediction_statistics():
    """Display prediction statistics with graphs that persist across navigation"""
    st.subheader("Prediction Statistics")
    
    if not st.session_state.history:
        st.info("No predictions made yet. Go to Predict page to make predictions.")
        return
    
    # Get prediction data and ensure graphs are regenerated
    history_df = pd.DataFrame(st.session_state.history)
    
    # Force graph regeneration by clearing any cached data
    if 'graph_cache_key' not in st.session_state:
        st.session_state.graph_cache_key = 0
    
    # Update cache key when new predictions are added
    current_prediction_count = len(st.session_state.history)
    if 'last_prediction_count' not in st.session_state:
        st.session_state.last_prediction_count = current_prediction_count
    
    if current_prediction_count != st.session_state.last_prediction_count:
        st.session_state.graph_cache_key += 1
        st.session_state.last_prediction_count = current_prediction_count
    
    # Create two columns for graphs
    col1, col2 = st.columns(2)
    
    with col1:
        # Graph 1: Churn vs Stay Predictions
        st.write("**Churn vs Stay Predictions**")
        
        # Calculate current statistics
        churn_count = len(history_df[history_df['lr_prediction'] == 1])
        stay_count = len(history_df[history_df['lr_prediction'] == 0])
        
        # Create fresh bar chart data
        prediction_data = pd.DataFrame({
            'Prediction': ['Stay', 'Churn'],
            'Count': [stay_count, churn_count]
        })
        
        # Display bar chart with unique key to force refresh
        st.bar_chart(
            prediction_data, 
            x='Prediction', 
            y='Count',
            use_container_width=True
        )
        
        # Show metrics
        st.metric("Total Predictions", len(history_df))
    
    with col2:
        # Graph 2: Model Agreement Analysis
        st.write("**Model Agreement Analysis**")
        
        # Calculate model agreements fresh each time
        agreements = 0
        disagreements = 0
        
        for _, row in history_df.iterrows():
            if row['lr_prediction'] == row['dt_prediction']:
                agreements += 1
            else:
                disagreements += 1
        
        # Create fresh agreement data
        agreement_data = pd.DataFrame({
            'Model Status': ['Agree', 'Disagree'],
            'Count': [agreements, disagreements]
        })
        
        # Display bar chart with unique key to force refresh
        st.bar_chart(
            agreement_data, 
            x='Model Status', 
            y='Count',
            use_container_width=True
        )
        
        # Show agreement percentage
        if len(history_df) > 0:
            agreement_rate = (agreements / len(history_df)) * 100
            st.metric("Model Agreement Rate", f"{agreement_rate:.1f}%")
    
    # Add refresh button for manual graph update
    if st.button("Refresh Graphs", help="Manually refresh the graphs"):
        st.session_state.graph_cache_key += 1
        st.rerun()
    
    # Show data persistence status
    st.info(f"Graphs updated with {len(history_df)} predictions. Data persists across all pages.")

