
import pandas as pd
import numpy as np

def run_multi_valuation(inputs, growth_rate, wacc, t_growth, market_data):
    """Integrates Pfizer script logic with SEC-audited data inputs"""
    
    # --- 1. DCF SECTION (Free Cash Flow to Firm) ---
    projection_years = 5
    rev = inputs['revenue']
    # Use audited EBIT margin or industry floor
    margin = inputs['ebit'] / inputs['revenue'] if inputs['revenue'] > 0 else 0.15
    
    projections = []
    for i in range(projection_years):
        rev *= (1 + growth_rate)
        ebit = rev * margin
        tax_impact = ebit * (1 - inputs['tax_rate'])
        
        # Pfizer Reinvestment Logic: Scaled CapEx proxy
        # FCFF = EBIT(1-t) + Depr - CapEx
        fcff = tax_impact + inputs['depr'] - (abs(inputs['capex']) * (rev/inputs['revenue']))
        
        pv = fcff / (1 + wacc)**(i+1)
        projections.append({'Year': 2026+i, 'Revenue': rev, 'FCFF': fcff, 'PV_FCFF': pv})
    
    df = pd.DataFrame(projections)
    
    # Gordon Growth Stability Check: WACC must be > t_growth
    if wacc <= t_growth:
        t_growth = wacc - 0.01
        
    tv = projections[-1]['FCFF'] * (1 + t_growth) / (wacc - t_growth)
    pv_tv = tv / (1 + wacc)**5
    
    ev = df['PV_FCFF'].sum() + pv_tv
    equity_dcf = ev - inputs['debt'] + inputs['cash']
    price_dcf = (equity_dcf * 1e6) / inputs['shares']

    # --- 2. DDM SECTION (Dividend Discount Model) ---
    # Cost of Equity (ke) via CAPM: Rf + Beta * ERP
    ke = market_data['rf'] + inputs.get('beta', 1.1) * (market_data['erp'])
    # Dividends per share converted from $M to absolute $
    dps = (inputs['dividends'] / inputs['shares']) * 1e6
    price_ddm = (dps * (1 + 0.02)) / (ke - 0.02) if ke > 0.02 else 0

    # --- 3. P/E SECTION (Relative Valuation) ---
    # Earnings per share converted from $M to absolute $
    eps = (inputs['net_income'] / inputs['shares']) * 1e6
    price_pe = eps * 15 # Baseline conservative P/E multiple

    return {
        "df": df,
        "dcf_price": price_dcf,
        "ddm_price": price_ddm,
        "pe_price": price_pe,
        "ev": ev,
        "current_price": inputs.get('current_price', 0)
    }

def calculate_sensitivity(inputs, growth_rate, wacc_range, g_range):
    """Generates an Enterprise Value matrix ($B) for heatmap visualization"""
    matrix = np.zeros((len(wacc_range), len(g_range)))
    market_data = {'rf': 0.045, 'erp': 0.055} # Standard sensitivity constants
    
    for i, w in enumerate(wacc_range):
        for j, g in enumerate(g_range):
            if w <= g:
                matrix[i, j] = np.nan
            else:
                res = run_multi_valuation(inputs, growth_rate, w, g, market_data)
                matrix[i, j] = res['ev'] / 1000 # Results in Billions for UI
                
    return matrix
