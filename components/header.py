
import streamlit as st

def header_component():
    """Professional gradient header with Prof. Bio"""
    CORPORATE_BLUE = "#002147"
    GOLD = "#FFD700"
    
    st.markdown(f"""
        <style>
        .main-header {{
            background: linear-gradient(135deg, {CORPORATE_BLUE} 0%, #004b8d 100%);
            padding: 2.5rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            border-bottom: 5px solid {GOLD};
        }}
        .bio-text {{
            font-size: 1.1rem;
            font-weight: 500;
            color: {GOLD};
            margin-top: 10px;
            letter-spacing: 1px;
        }}
        </style>
        <div class="main-header">
            <h1 style="margin: 0; font-size: 2.5rem; color: white;">THE MOUNTAIN PATH</h1>
            <h2 style="margin: 5px 0; font-size: 1.5rem; opacity: 0.9; color: white;">Institutional Equity Valuation Terminal</h2>
            <p class="bio-text">
                Prof. V. Ravichandran | 28+ Years Finance Experience | 10+ Years Academic Excellence
            </p>
        </div>
    """, unsafe_allow_html=True)
