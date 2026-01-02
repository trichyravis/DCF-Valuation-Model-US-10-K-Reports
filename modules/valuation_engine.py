
import pandas as pd
import numpy as np

def run_multi_valuation(inputs, growth_rate, wacc, t_growth, market_data):
    """Institutional Valuation using NOPAT and Reinvestment Rates"""
    rev = inputs['revenue']
    ebit = inputs['ebit']
    tax_rate = inputs.get('tax_rate', 0.21)
    
    # Growth must be funded. Reinvestment Rate = Growth / Return on Capital (ROC)
    # We assume a standard 15% ROC for large-cap tech.
    assumed_roc = 0.15 
    reinvestment_rate = min(growth_rate / assumed_roc, 0.80) 

    projections = []
    for i in range(5):
        rev *= (1 + growth_rate)
        year_ebit = rev * (ebit / inputs['revenue']) if inputs['revenue'] > 0 else 0
        year_nopat = year_ebit * (1 - tax_rate)
        
        # FCFF = NOPAT * (1 - Reinvestment Rate)
        fcff = year_nopat * (1 - reinvestment_rate)
        pv = fcff / (1 + wacc)**(i + 1)
        
        projections.append({'Year': 2026+i, 'Revenue': rev, 'FCFF': fcff, 'PV_FCFF': pv})
    
    df = pd.DataFrame(projections)
    
    # Terminal Value stability guard
    stable_wacc = max(wacc, t_growth + 0.01)
    terminal_value = (projections[-1]['FCFF'] * (1 + t_growth)) / (stable_wacc - t_growth)
    pv_terminal = terminal_value / (1 + stable_wacc)**5
    
    ev = df['PV_FCFF'].sum() + pv_terminal
    equity_value = ev - inputs['debt'] + inputs['cash']
    price_dcf = (equity_value * 1e6) / inputs['shares'] if inputs['shares'] > 0 else 0

    # Earnings Multiple
    eps = (inputs['net_income'] / inputs['shares']) * 1e6 if inputs['shares'] > 0 else 0
    price_pe = eps * 15 

    return {
        "df": df, "dcf_price": price_dcf, "pe_price": price_pe,
        "ev": ev, "pv_terminal": pv_terminal, 
        "current_price": inputs['current_price'], "ddm_price": 0
    }

def calculate_sensitivity(inputs, growth_rate, wacc_range, g_range):
    """Generates the Enterprise Value matrix for the heatmap"""
    matrix = np.zeros((len(wacc_range), len(g_range)))
    market_data = {'rf': 0.045, 'erp': 0.055} 
    
    for i, w in enumerate(wacc_range):
        for j, g in enumerate(g_range):
            if w <= g:
                matrix[i, j] = np.nan
            else:
                res = run_multi_valuation(inputs, growth_rate, w, g, market_data)
                matrix[i, j] = res['ev'] / 1000 # Return in Billions
                
    return matrix
