
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import os

# --- 1. IMPORT CUSTOM MODULES ---
from components.header import header_component
from components.sidebar import sidebar_component
from components.footer import footer_component
from content.about_text import ABOUT_CONTENT
from content.valuation_qa import VALUATION_QA
from modules.data_fetcher import SECDataFetcher
from modules.valuation_engine import run_dcf_engine, calculate_sensitivity

# --- 2. INITIALIZATION & CONFIG ---
st.set_page_config(
    page_title="Mountain Path | Equity Valuation Terminal",
    page_icon="🏔️",
    layout="wide"
)

# Ensure reports directory exists
if not os.path.exists('reports'):
    os.makedirs('reports')

# --- 3. UI COMPONENTS ---
header_component()
ticker, growth_rate, wacc_base, t_growth, run_btn = sidebar_component()

# --- 4. MAIN APP LOGIC ---
if run_btn:
    with st.spinner(f"🔍 Accessing SEC Filings for {ticker}..."):
        fetcher = SECDataFetcher(ticker)
        inputs = fetcher.get_valuation_inputs()
    
    if inputs:
        st.success(f"✅ Data retrieved for {inputs['name']}")
        
        # Run Valuation Engine
        df_projections, enterprise_value, equity_value, implied_price = run_dcf_engine(
            inputs, growth_rate, wacc_base, t_growth
        )

        # High-Level Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Enterprise Value", f"${enterprise_value/1000:.2f}B")
        m2.metric("Equity Value", f"${equity_value/1000:.2f}B")
        m3.metric("Implied Share Price", f"${implied_price:.2f}")
        # Note: Net Debt = Debt - Cash
        m4.metric("Net Debt", f"${(inputs['debt'] - inputs['cash']):,.0f}M", delta_color="inverse")

        # --- TABS FOR DETAILED ANALYSIS ---
        tabs = st.tabs(["📊 Financial Projections", "🔥 Sensitivity Analysis", "📖 Methodology", "🎓 Masterclass"])

        with tabs[0]:
            st.subheader(f"5-Year FCFF Forecast: {ticker}")
            # Format dataframe for display
            display_df = df_projections.copy()
            for col in ['Revenue', 'FCFF', 'PV_FCFF']:
                display_df[col] = display_df[col].map("${:,.2f}M".format)
            
            st.table(display_df)
            
            # Export Option
            csv = df_projections.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download Projection CSV",
                data=csv,
                file_name=f"Valuation_{ticker}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime='text/csv'
            )

        with tabs[1]:
            st.subheader("Bivariate Sensitivity Analysis (Enterprise Value $B)")
            st.info("How the valuation changes with WACC and Terminal Growth variations.")
            
            # Generate ranges for sensitivity
            w_range = [wacc_base - 0.01, wacc_base - 0.005, wacc_base, wacc_base + 0.005, wacc_base + 0.01]
            g_range = [t_growth - 0.005, t_growth, t_growth + 0.005]
            
            matrix = calculate_sensitivity(inputs, growth_rate, w_range, g_range)
            
            # Heatmap Visualization
            sens_df = pd.DataFrame(
                matrix, 
                index=[f"{x*100:.1f}%" for x in w_range], 
                columns=[f"{x*100:.1f}%" for x in g_range]
            )
            
            fig = px.imshow(
                sens_df,
                labels=dict(x="Terminal Growth", y="WACC", color="EV ($B)"),
                x=[f"{x*100:.1f}%" for x in g_range],
                y=[f"{x*100:.1f}%" for x in w_range],
                text_auto=".1f",
                aspect="auto",
                color_continuous_scale='YlGnBu'
            )
            st.plotly_chart(fig, use_container_width=True)

        with tabs[2]:
            st.header("📖 Valuation Methodology")
            st.write(ABOUT_CONTENT["intro"])
            st.markdown(ABOUT_CONTENT["workflow"])
            
            c1, c2, c3 = st.columns(3)
            with c1: st.info(ABOUT_CONTENT["arima"]) # Stage 1 Info
            with c2: st.info(ABOUT_CONTENT["vasicek"]) # WACC Info
            with c3: st.info(ABOUT_CONTENT["cir"]) # Terminal Info

        with tabs[3]:
            st.header("🎓 Equity Research Masterclass")
            for q, a in VALUATION_QA:
                with st.expander(q):
                    st.write(a)

    else:
        st.error(f"⚠️ Unable to fetch data for ticker '{ticker}'. Please check the symbol and try again.")

else:
    # Landing State
    st.info("👈 Enter a US Ticker (e.g., AAPL, MSFT, NVDA) and click 'Execute Audited DCF' to begin.")
    
    # Optional: Display a diagram showing the DCF logic while waiting
    

# --- 5. FOOTER ---
footer_component()
