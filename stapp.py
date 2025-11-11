import streamlit as st
from difflib import SequenceMatcher
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Name Match API", page_icon="🔍", layout="centered")

# Custom CSS for professional look
st.markdown("""
    <style>
    .main {
        max-width: 800px;
        margin: 0 auto;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        height: 3em;
        font-size: 16px;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        margin-top: 20px;
    }
    .stButton>button:hover {
        background-color: #45a049;
        border: none;
    }
    div[data-testid="stTextInput"] > label {
        font-weight: 600;
        color: #333;
    }
    .score-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 12px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .score-value {
        font-size: 60px;
        font-weight: bold;
        color: white;
        margin: 10px 0;
    }
    .score-label {
        font-size: 18px;
        color: #f0f0f0;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

def calculate_match_score(name1_parts, name2_parts):
    """Calculate similarity score between two names using difflib"""
    # Combine name parts
    name1 = " ".join(filter(None, name1_parts)).strip().lower()
    name2 = " ".join(filter(None, name2_parts)).strip().lower()
    
    if not name1 or not name2:
        return 0
    
    # Calculate similarity ratio
    ratio = SequenceMatcher(None, name1, name2).ratio()
    return round(ratio * 100, 2)

def get_confidence_level(score):
    """Return confidence level based on score"""
    if score >= 90:
        return "Excellent Match", "#4CAF50"
    elif score >= 75:
        return "Good Match", "#8BC34A"
    elif score >= 60:
        return "Moderate Match", "#FFC107"
    elif score >= 40:
        return "Low Match", "#FF9800"
    else:
        return "Poor Match", "#F44336"

def create_gauge_chart(score):
    """Create a professional gauge chart for the score"""
    confidence, color = get_confidence_level(score)
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': confidence, 'font': {'size': 24, 'color': color}},
        number = {'suffix': "%", 'font': {'size': 50}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "darkgray"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#ffebee'},
                {'range': [40, 60], 'color': '#fff3e0'},
                {'range': [60, 75], 'color': '#fff9c4'},
                {'range': [75, 90], 'color': '#f1f8e9'},
                {'range': [90, 100], 'color': '#e8f5e9'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 95
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'family': "Arial, sans-serif"}
    )
    
    return fig

# Header
st.title("🔍 Name Match API")
st.markdown("**Compare two names and calculate their similarity score**")
st.markdown("---")

# Create two columns for the input forms
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Name 1")
    name1_first = st.text_input("First Name", key="name1_first", placeholder="Enter first name")
    name1_middle = st.text_input("Middle Name", key="name1_middle", placeholder="Enter middle name")
    name1_last = st.text_input("Last Name", key="name1_last", placeholder="Enter last name")

with col2:
    st.subheader("📋 Name 2")
    name2_first = st.text_input("First Name", key="name2_first", placeholder="Enter first name")
    name2_middle = st.text_input("Middle Name", key="name2_middle", placeholder="Enter middle name")
    name2_last = st.text_input("Last Name", key="name2_last", placeholder="Enter last name")

# Submit button
if st.button("🔄 Calculate Match Score"):
    # Validate inputs
    name1_parts = [name1_first, name1_middle, name1_last]
    name2_parts = [name2_first, name2_middle, name2_last]
    
    if not any(name1_parts) or not any(name2_parts):
        st.error("⚠️ Please enter at least one name field for both Name 1 and Name 2")
    else:
        # Calculate score
        score = calculate_match_score(name1_parts, name2_parts)
        
        # Display full names being compared
        full_name1 = " ".join(filter(None, name1_parts))
        full_name2 = " ".join(filter(None, name2_parts))
        
        st.markdown("---")
        st.markdown("### 📊 Comparison Results")
        
        # Show names being compared
        comp_col1, comp_col2 = st.columns(2)
        with comp_col1:
            st.info(f"**Name 1:** {full_name1}")
        with comp_col2:
            st.info(f"**Name 2:** {full_name2}")
        
        # Display gauge chart
        fig = create_gauge_chart(score)
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional insights
        confidence, color = get_confidence_level(score)
        
        if score >= 90:
            st.success("✅ The names are nearly identical or very similar.")
        elif score >= 75:
            st.success("✓ The names show strong similarity.")
        elif score >= 60:
            st.warning("⚠️ The names have moderate similarity.")
        elif score >= 40:
            st.warning("⚠️ The names have low similarity.")
        else:
            st.error("❌ The names are significantly different.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 14px;'>
        <p>Powered by Python's difflib SequenceMatcher Algorithm</p>
    </div>
""", unsafe_allow_html=True)
