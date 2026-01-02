
import pandas as pd
import numpy as np

def run_multi_valuation(inputs, growth_rate, wacc, t_growth, market_data):
    """Integrates Pfizer script logic into the terminal engine"""
    
    # --- 1. DCF SECTION ---
    projection_years = 5
    rev = inputs['revenue']
    margin = inputs['ebit'] / inputs['revenue'] if inputs['revenue'] > 0 else 0.15
    
    projections = []
    for i in range(projection_years):
        rev *= (1 + growth_rate)
        ebit = rev * margin
        tax_impact = ebit * (1 - inputs['tax_rate'])
        # Pfizer script logic: Reinvestment proxy (CapEx + WC)
        fcff = tax_impact + inputs['depr'] - (inputs['capex'] * (rev/inputs['revenue']))
        
        pv = fcff / (1 + wacc)**(i+1)
        projections.append({'Year': 2026+i, 'FCFF': fcff, 'PV_FCFF': pv})
    
    df = pd.DataFrame(projections)
    tv = projections[-1]['FCFF'] * (1 + t_growth) / (wacc - t_growth)
    pv_tv = tv / (1 + wacc)**5
    
    ev = df['PV_FCFF'].sum() + pv_tv
    equity_dcf = ev - inputs['debt'] + inputs['cash']
    price_dcf = (equity_dcf * 1e6) / inputs['shares']

    # --- 2. DDM SECTION ---
    # Cost of Equity calculation (CAPM)
    ke = market_data['rf'] + inputs.get('beta', 1.0) * (market_data['erp'])
    dps = (inputs['dividends'] / inputs['shares']) * 1e6
    price_ddm = (dps * (1 + 0.02)) / (ke - 0.02) if ke > 0.02 else 0

    # --- 3. P/E SECTION ---
    eps = (inputs['net_income'] / inputs['shares']) * 1e6
    price_pe = eps * 15 # Using conservative 15x multiple

    return {
        "df": df,
        "dcf_price": price_dcf,
        "ddm_price": price_ddm,
        "pe_price": price_pe,
        "ev": ev
    }
