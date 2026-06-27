import streamlit as st
import pandas as pd

def show_history():
    """Display history page with all past predictions"""
    st.title("Prediction History")
    st.write("View all past predictions")
    
    if st.session_state.history:
        # Convert history to DataFrame
        history_df = pd.DataFrame(st.session_state.history)
        
        # Statistics
        st.subheader("Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_predictions = len(history_df)
            st.metric("Total Predictions", total_predictions)
        
        with col2:
            churn_predictions = len(history_df[history_df['lr_prediction'] == 1])
            st.metric("Churn Predictions", churn_predictions)
        
        with col3:
            stay_predictions = len(history_df[history_df['lr_prediction'] == 0])
            st.metric("Stay Predictions", stay_predictions)
        
        # History table
        st.subheader("Prediction History")
        display_df = history_df[['age', 'tenure', 'monthly_charges', 'lr_result', 'dt_result', 'timestamp']]
        st.dataframe(display_df, use_container_width=True)
        
        # Clear history button
        if st.button("Clear History"):
            st.session_state.history = []
            st.success("History cleared!")
            st.rerun()
    else:
        st.info("No predictions yet. Go to Predict page to make predictions.")
