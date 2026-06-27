import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import BACKEND_URL

def show_predict():
    """Display prediction page with customer input and results"""
    st.title("Predict Customer Churn")
    st.write("Enter customer information to get churn predictions")
    
    # ==================== LAST PREDICTION SECTION ====================
    show_last_prediction()
    
    # ==================== ACTIVE MODEL STATUS ====================
    show_active_model_status()
    
    # ==================== INPUT SECTION ====================
    show_input_section()
    
    # ==================== PREDICTION SECTION ====================
    show_prediction_section()

def show_last_prediction():
    """Display last prediction results if available"""
    # Check if we have a previous prediction saved in session state
    # This restores the prediction when returning to the page
    if st.session_state.get('last_prediction_result'):
        # Show message that we're restoring saved data
        st.info("💾 Showing your saved prediction results")
        st.subheader("Last Prediction Result")
        
        last_result = st.session_state.last_prediction_result
        last_input = st.session_state.last_prediction_input
        
        # Show last input data
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Last Age", last_input['age'])
        with col2:
            st.metric("Last Tenure", f"{last_input['tenure']} months")
        with col3:
            st.metric("Last Charges", f"${last_input['monthly_charges']}")
        
        # Show last prediction results
        st.write("**Last Prediction Results:**")
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"Logistic Regression: {last_result['lr_result']}")
        with col2:
            st.success(f"Decision Tree: {last_result['dt_result']}")
        
        # Show last probability
        if 'probability' in last_result:
            stay_prob = last_result['probability'][0] * 100
            churn_prob = last_result['probability'][1] * 100
            st.info(f"Stay Probability: {stay_prob:.1f}%, Churn Probability: {churn_prob:.1f}%")
            
            # Show probability bar chart - this makes the graph persist!
            st.subheader("Churn Probability Chart")
            prob_data = pd.DataFrame({
                'Outcome': ['Stay', 'Churn'],
                'Probability': last_result['probability']
            })
            st.bar_chart(prob_data, x='Outcome', y='Probability')
    else:
        # No prediction made yet - show helpful message
        st.info("🔮 Make a prediction below and it will be saved automatically!")

def show_active_model_status():
    """Show which model is currently active"""
    if st.session_state.get('training_completed') and st.session_state.get('active_model'):
        active_model = st.session_state.active_model
        st.info(f"**Active Model**: {active_model} is being used for predictions")
        st.write("This model was selected based on highest accuracy during training.")

def show_input_section():
    """Display input section with all customer information fields"""
    st.subheader("Customer Information")
    
    # Get last input values from session state or use defaults
    last_input = st.session_state.get('last_prediction_input', {})
    
    # ==================== PERSONAL INFORMATION ====================
    st.write("**Personal Information**")
    col1, col2 = st.columns(2)
    
    with col1:
        # Age - required field (18-100 years)
        age = st.number_input(
            "Age *", 
            min_value=18, 
            max_value=100, 
            value=last_input.get('age', 30), 
            step=1,
            help="Customer age in years (required)"
        )
    
    with col2:
        # Gender - Male or Female
        gender = st.selectbox(
            "Gender",
            options=["Male", "Female"],
            index=0 if last_input.get('gender', 'Male') == 'Male' else 1,
            help="Customer gender"
        )
    
    # ==================== SERVICE INFORMATION ====================
    st.write("**Service Information**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Tenure - how many months with company (required)
        tenure = st.number_input(
            "Tenure (months) *",
            min_value=0,
            max_value=120,
            value=last_input.get('tenure', 12),
            step=1,
            help="Months with company (required)"
        )
    
    with col2:
        # Monthly Charges - what they pay each month (required)
        monthly_charges = st.number_input(
            "Monthly Charges ($) *",
            min_value=0.0,
            max_value=200.0,
            value=last_input.get('monthly_charges', 50.0),
            step=5.0,
            help="Monthly bill amount (required)"
        )
    
    with col3:
        # Total Charges - total paid so far
        total_charges = st.number_input(
            "Total Charges ($)",
            min_value=0.0,
            max_value=10000.0,
            value=last_input.get('total_charges', monthly_charges * tenure),
            step=10.0,
            help="Total amount paid so far"
        )
    
    # ==================== CONTRACT & SERVICES ====================
    st.write("**Contract & Services**")
    col1, col2 = st.columns(2)
    
    with col1:
        # Contract Type - Month-to-month, One year, or Two year
        contract = st.selectbox(
            "Contract Type",
            options=["Month-to-month", "One year", "Two year"],
            index=["Month-to-month", "One year", "Two year"].index(last_input.get('contract', 'Month-to-month')),
            help="Type of contract"
        )
        
        # Payment Method - how they pay
        payment_method = st.selectbox(
            "Payment Method",
            options=["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
            index=["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"].index(last_input.get('payment_method', 'Electronic check')),
            help="How customer pays bill"
        )
    
    with col2:
        # Internet Service - DSL, Fiber optic, or No
        internet_service = st.selectbox(
            "Internet Service",
            options=["DSL", "Fiber optic", "No"],
            index=["DSL", "Fiber optic", "No"].index(last_input.get('internet_service', 'Fiber optic')),
            help="Type of internet connection"
        )
        
        # Phone Service - Yes or No
        phone_service = st.selectbox(
            "Phone Service",
            options=["Yes", "No"],
            index=0 if last_input.get('phone_service', 'Yes') == 'Yes' else 1,
            help="Do they have phone service?"
        )
    
    # ==================== ADDITIONAL SERVICES ====================
    st.write("**Additional Services**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Multiple Lines - Yes or No
        multiple_lines = st.selectbox(
            "Multiple Lines",
            options=["Yes", "No"],
            index=0 if last_input.get('multiple_lines', 'No') == 'Yes' else 1,
            help="Multiple phone lines"
        )
        
        # Online Security - Yes or No
        online_security = st.selectbox(
            "Online Security",
            options=["Yes", "No"],
            index=0 if last_input.get('online_security', 'No') == 'Yes' else 1,
            help="Online security service"
        )
    
    with col2:
        # Online Backup - Yes or No
        online_backup = st.selectbox(
            "Online Backup",
            options=["Yes", "No"],
            index=0 if last_input.get('online_backup', 'No') == 'Yes' else 1,
            help="Online backup service"
        )
        
        # Device Protection - Yes or No
        device_protection = st.selectbox(
            "Device Protection",
            options=["Yes", "No"],
            index=0 if last_input.get('device_protection', 'No') == 'Yes' else 1,
            help="Device protection plan"
        )
    
    with col3:
        # Tech Support - Yes or No
        tech_support = st.selectbox(
            "Tech Support",
            options=["Yes", "No"],
            index=0 if last_input.get('tech_support', 'No') == 'Yes' else 1,
            help="Technical support service"
        )
        
        # Streaming TV - Yes or No
        streaming_tv = st.selectbox(
            "Streaming TV",
            options=["Yes", "No"],
            index=0 if last_input.get('streaming_tv', 'No') == 'Yes' else 1,
            help="TV streaming service"
        )
    
    with col4:
        # Streaming Movies - Yes or No
        streaming_movies = st.selectbox(
            "Streaming Movies",
            options=["Yes", "No"],
            index=0 if last_input.get('streaming_movies', 'No') == 'Yes' else 1,
            help="Movie streaming service"
        )
        
        # Paperless Billing - Yes or No
        paperless_billing = st.selectbox(
            "Paperless Billing",
            options=["Yes", "No"],
            index=0 if last_input.get('paperless_billing', 'No') == 'Yes' else 1,
            help="Electronic billing instead of paper"
        )
    
    # Store ALL current inputs in session state
    # This saves everything so it persists when switching pages
    st.session_state.current_input = {
        'age': age,
        'gender': gender,
        'tenure': tenure,
        'monthly_charges': monthly_charges,
        'total_charges': total_charges,
        'contract': contract,
        'payment_method': payment_method,
        'internet_service': internet_service,
        'phone_service': phone_service,
        'multiple_lines': multiple_lines,
        'online_security': online_security,
        'online_backup': online_backup,
        'device_protection': device_protection,
        'tech_support': tech_support,
        'streaming_tv': streaming_tv,
        'streaming_movies': streaming_movies,
        'paperless_billing': paperless_billing
    }

def show_prediction_section():
    """Handle prediction logic with all customer data"""
    # Prediction button
    if st.button("Predict", type="primary"):
        # Get current input with all fields
        current_input = st.session_state.get('current_input', {
            'age': 30,
            'gender': 'Male',
            'tenure': 12,
            'monthly_charges': 50.0,
            'total_charges': 600.0,
            'contract': 'Month-to-month',
            'payment_method': 'Electronic check',
            'internet_service': 'Fiber optic',
            'phone_service': 'Yes',
            'multiple_lines': 'No',
            'online_security': 'No',
            'online_backup': 'No',
            'device_protection': 'No',
            'tech_support': 'No',
            'streaming_tv': 'No',
            'streaming_movies': 'No',
            'paperless_billing': 'No'
        })
        
        # Prepare data for API request with all fields
        # Note: Backend may not use all fields yet, but we send them for future use
        data = {
            "age": current_input['age'],
            "tenure": current_input['tenure'],
            "monthly_charges": current_input['monthly_charges'],
            # Additional fields (backend can ignore these if not implemented)
            "gender": current_input.get('gender', 'Male'),
            "total_charges": current_input.get('total_charges', 0),
            "contract": current_input.get('contract', 'Month-to-month'),
            "payment_method": current_input.get('payment_method', 'Electronic check'),
            "internet_service": current_input.get('internet_service', 'Fiber optic'),
            "phone_service": current_input.get('phone_service', 'Yes'),
            "multiple_lines": current_input.get('multiple_lines', 'No'),
            "online_security": current_input.get('online_security', 'No'),
            "online_backup": current_input.get('online_backup', 'No'),
            "device_protection": current_input.get('device_protection', 'No'),
            "tech_support": current_input.get('tech_support', 'No'),
            "streaming_tv": current_input.get('streaming_tv', 'No'),
            "streaming_movies": current_input.get('streaming_movies', 'No'),
            "paperless_billing": current_input.get('paperless_billing', 'No')
        }
        
        try:
            # Send prediction request to Flask API
            response = requests.post(f"{BACKEND_URL}/predict", json=data)
            result = response.json()
            
            # Display results
            st.subheader("Prediction Results")
            
            # Show model predictions in cards
            col1, col2 = st.columns(2)
            
            with col1:
                lr_result = "Churn" if result['lr_prediction'] == 1 else "Stay"
                st.success(f"Logistic Regression: {lr_result}")
            
            with col2:
                dt_result = "Churn" if result['dt_prediction'] == 1 else "Stay"
                st.success(f"Decision Tree: {dt_result}")
            
            # Show probability bar chart
            st.subheader("Churn Probability (Logistic Regression)")
            
            prob_data = pd.DataFrame({
                'Outcome': ['Stay', 'Churn'],
                'Probability': result['probability']
            })
            
            # Create bar chart
            st.bar_chart(prob_data, x='Outcome', y='Probability')
            
            # Show probability percentages
            stay_prob = result['probability'][0] * 100
            churn_prob = result['probability'][1] * 100
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Stay Probability", f"{stay_prob:.1f}%")
            with col2:
                st.metric("Churn Probability", f"{churn_prob:.1f}%")
            
            # Save prediction to session state and history
            save_prediction_result(current_input, result, lr_result, dt_result)
                
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to backend API. Please make sure the Flask server is running on http://localhost:5000")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def save_prediction_result(input_data, result, lr_result, dt_result):
    """Save prediction result to session state and history with all fields"""
    # Save last prediction for persistence (includes ALL fields)
    st.session_state.last_prediction_input = input_data
    st.session_state.last_prediction_result = {
        'lr_prediction': result['lr_prediction'],
        'dt_prediction': result['dt_prediction'],
        'lr_result': lr_result,
        'dt_result': dt_result,
        'probability': result['probability']
    }
    
    # Save to history with all customer information
    prediction_record = {
        # Personal Information
        'age': input_data['age'],
        'gender': input_data.get('gender', 'Male'),
        
        # Service Information
        'tenure': input_data['tenure'],
        'monthly_charges': input_data['monthly_charges'],
        'total_charges': input_data.get('total_charges', 0),
        
        # Contract & Services
        'contract': input_data.get('contract', 'Month-to-month'),
        'payment_method': input_data.get('payment_method', 'Electronic check'),
        'internet_service': input_data.get('internet_service', 'Fiber optic'),
        'phone_service': input_data.get('phone_service', 'Yes'),
        
        # Additional Services
        'multiple_lines': input_data.get('multiple_lines', 'No'),
        'online_security': input_data.get('online_security', 'No'),
        'online_backup': input_data.get('online_backup', 'No'),
        'device_protection': input_data.get('device_protection', 'No'),
        'tech_support': input_data.get('tech_support', 'No'),
        'streaming_tv': input_data.get('streaming_tv', 'No'),
        'streaming_movies': input_data.get('streaming_movies', 'No'),
        'paperless_billing': input_data.get('paperless_billing', 'No'),
        
        # Prediction Results
        'lr_prediction': result['lr_prediction'],
        'dt_prediction': result['dt_prediction'],
        'lr_result': lr_result,
        'dt_result': dt_result,
        'probability': result['probability'],
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.history.append(prediction_record)
    
    st.success("✅ Prediction saved! All customer data is preserved across pages.")
