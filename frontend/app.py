import streamlit as st
from components import dashboard, train, predict, history

# ==================== CONFIGURATION ====================
def initialize_app():
    """Initialize app configuration and session state"""
    # Initialize all session state variables for data persistence
    initialize_session_state()
    
    # Page configuration
    st.set_page_config(
        page_title="Churn Prediction Dashboard", 
        layout="wide",
        initial_sidebar_state="expanded"
    )

def initialize_session_state():
    """Initialize all session state variables for data persistence"""
    # Prediction history
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    # Training data persistence
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False
    if 'uploaded_data' not in st.session_state:
        st.session_state.uploaded_data = None
    
    # Active model information
    if 'active_model' not in st.session_state:
        st.session_state.active_model = None
    if 'active_accuracy' not in st.session_state:
        st.session_state.active_accuracy = None
    if 'model_accuracies' not in st.session_state:
        st.session_state.model_accuracies = {}
    
    # Prediction input persistence
    if 'last_prediction_input' not in st.session_state:
        st.session_state.last_prediction_input = {
            'age': 30,
            'tenure': 12,
            'monthly_charges': 50.0
        }
    if 'last_prediction_result' not in st.session_state:
        st.session_state.last_prediction_result = None
    
    # Training completion flag
    if 'training_completed' not in st.session_state:
        st.session_state.training_completed = False
    
    # Graph persistence variables
    if 'graph_cache_key' not in st.session_state:
        st.session_state.graph_cache_key = 0
    if 'last_prediction_count' not in st.session_state:
        st.session_state.last_prediction_count = 0

# ==================== STYLING ====================
def apply_custom_styles():
    """Apply custom CSS for professional sidebar styling"""
    # Load CSS from external file
    with open('static/style.css', 'r') as f:
        css_content = f.read()
    
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
def create_sidebar():
    """Create sidebar navigation with professional styling"""
    # Sidebar title
    st.sidebar.markdown("""
    # <h1 style='color: white; text-align: center; font-size: 24px; margin-bottom: 30px;'> 
    #     Customer Churn Predictor 
    # </h1>
    """, unsafe_allow_html=True)
    
    # Navigation options
    page = st.sidebar.radio("Navigate to:", [
        "Dashboard",
        "Train Models", 
        "Predict",
        "History"
    ], index=0)
    
    return page

# ==================== PAGE ROUTING ====================
def route_to_page(page):
    """Route to the appropriate page based on selection"""
    if page == "Dashboard":
        dashboard.show_dashboard()
    elif page == "Train Models":
        train.show_train()
    elif page == "Predict":
        predict.show_predict()
    elif page == "History":
        history.show_history()

# ==================== FOOTER ====================
def show_footer():
    """Display application footer"""
    st.markdown("---")
    st.write("Built with Flask, Streamlit, and Machine Learning")

# ==================== MAIN APP ====================
def main():
    """Main application entry point"""
    # Initialize app
    initialize_app()
    
    # Apply custom styles
    apply_custom_styles()
    
    # Create sidebar
    page = create_sidebar()
    
    # Route to appropriate page
    route_to_page(page)
    
    # Show footer
    show_footer()

# Run the main app
if __name__ == "__main__":
    main()
