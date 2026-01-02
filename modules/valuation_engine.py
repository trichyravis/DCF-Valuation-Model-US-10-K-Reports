
import pandas as pd
import numpy as np

def run_multi_valuation(inputs, growth_rate, wacc, t_growth, market_data):
    """
    Institutional Multi-Method Valuation Engine
    Calculates: DCF (FCFF), DDM (Dividend Discount), and Relative P/E Valuation
    """
    # --- 1. DCF SECTION (Two-Stage Free Cash Flow to Firm) ---
    projection_years = 5
    rev = inputs['revenue']
    
    # EBIT Margin from audited data or industry floor
    margin = inputs['ebit'] / inputs['revenue'] if inputs['revenue'] > 0 else 0.15
    tax_rate = inputs.get('tax_rate', 0.21)
    
    projections = []
    for i in range(projection_years):
        rev *= (1 + growth_rate)
        year_ebit = rev * margin
        year_nopat = year_ebit * (1 - tax_rate)
        
        # FCFF = NOPAT - Reinvestment (Simplified proxy)
        # Using a standard 30% reinvestment rate for growth
        fcff = year_nopat * 0.7 
        
        pv_factor = 1 / (1 + wacc)**(i + 1)
        pv_fcff = fcff * pv_factor
        
        projections.append({
            'Year': 2026 + i, 
            'Revenue': rev, 
            'FCFF': fcff, 
            'PV_FCFF': pv_fcff
        })
    
    df = pd.DataFrame(projections)
    
    # Terminal Value Guard
    stable_wacc = max(wacc, t_growth + 0.01)
    last_fcff = projections[-1]['FCFF']
    terminal_value = (last_fcff * (1 + t_growth)) / (stable_wacc - t_growth)
    pv_terminal = terminal_value / (1 + stable_wacc)**projection_years
    
    # Enterprise Value (EV) and Equity Value
    ev = df['PV_FCFF'].sum() + pv_terminal
    equity_value = ev - inputs['debt'] + inputs['cash']
    price_dcf = (equity_value * 1e6) / inputs['shares'] if inputs['shares'] > 0 else 0

    # --- 2. DDM & P/E Valuations ---
    beta = inputs.get('beta', 1.1)
    ke = market_data['rf'] + (beta * market_data['erp'])
    dps = (inputs['dividends'] / inputs['shares']) * 1e6 if inputs['shares'] > 0 else 0
    price_ddm = (dps * (1 + 0.02)) / (ke - 0.02) if ke > 0.02 else 0
    
    eps = (inputs['net_income'] / inputs['shares']) * 1e6 if inputs['shares'] > 0 else 0
    price_pe = eps * 15 # baseline conservative P/E multiple

    return {
        "df": df,
        "dcf_price": price_dcf,
        "ddm_price": price_ddm,
        "pe_price": price_pe,
        "ev": ev,
        "pv_terminal": pv_terminal
    }

def calculate_sensitivity(inputs, growth_rate, wacc_range, g_range):
    """
    Generates an Enterprise Value matrix ($B) for heatmap visualization
    This is the missing function causing your ImportError.
    """
    matrix = np.zeros((len(wacc_range), len(g_range)))
    # Standard sensitivity constants
    market_data = {'rf': 0.045, 'erp': 0.055} 
    
    for i, w in enumerate(wacc_range):
        for j, g in enumerate(g_range):
            if w <= g:
                matrix[i, j] = np.nan
            else:
                res = run_multi_valuation(inputs, growth_rate, w, g, market_data)
                # Results in Billions for the UI heatmap
                matrix[i, j] = res['ev'] / 1000 
                
    return matrix
