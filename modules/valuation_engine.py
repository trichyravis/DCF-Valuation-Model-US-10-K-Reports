
import pandas as pd
import numpy as np


def run_multi_valuation(inputs, growth_rate, wacc, t_growth, market_data):
    """
    Institutional Valuation Logic:
    1. Projections based on NOPAT & Reinvestment Rate
    2. Enterprise Value (Total Firm Value) in Millions
    3. Equity Value Bridge (Subtract Debt, Add Cash)
    4. Fair Value (Per Share) in absolute Dollars
    """
    # --- 1. SETUP ---
    # Inputs are already in Millions ($M) from SECDataFetcher
    rev = inputs['revenue']
    ebit = inputs['ebit']
    tax_rate = inputs.get('tax_rate', 0.21)
    shares_m = inputs['shares'] / 1e6  # Convert absolute shares to Millions
    
    # Fundamental Finance: To grow, you must reinvest.
    # We assume a 15% Return on Capital (ROC) for Alphabet.
    # Reinvestment Rate = Growth / ROC
    assumed_roc = 0.15
    reinvestment_rate = min(growth_rate / assumed_roc, 0.80)

    # --- 2. 5-YEAR PROJECTION (STAGE 1) ---
    projections = []
    current_rev = rev
    
    for i in range(5):
        current_rev *= (1 + growth_rate)
        # Assume constant EBIT margin from current audited data
        year_ebit = current_rev * (ebit / rev) if rev > 0 else 0
        year_nopat = year_ebit * (1 - tax_rate)
        
        # FCFF = NOPAT - Reinvestment
        # This prevents negative cash flows if the company is profitable
        fcff = year_nopat * (1 - reinvestment_rate)
        
        pv_factor = 1 / (1 + wacc)**(i + 1)
        pv_fcff = fcff * pv_factor
        
        projections.append({
            'Year': 2026 + i,
            'Revenue': current_rev,
            'FCFF': fcff,
            'PV_FCFF': pv_fcff
        })
    
    df = pd.DataFrame(projections)

    # --- 3. TERMINAL VALUE (STAGE 2) ---
    # Gordon Growth: WACC must be > t_growth
    stable_wacc = max(wacc, t_growth + 0.01)
    last_fcff = projections[-1]['FCFF']
    
    terminal_value = (last_fcff * (1 + t_growth)) / (stable_wacc - t_growth)
    pv_terminal = terminal_value / (1 + stable_wacc)**5
    
    # --- 4. THE VALUATION BRIDGE (Unit Safety) ---
    # Enterprise Value (EV) in $M
    ev_m = df['PV_FCFF'].sum() + pv_terminal
    
    # Equity Value = EV - Debt + Cash
    equity_val_m = ev_m - inputs['debt'] + inputs['cash']
    
    # Fair Value Per Share = (Equity Value in Millions / Shares in Millions)
    # This ensures the result is in actual Dollars (e.g., $150.00)
    price_dcf = equity_val_m / shares_m if shares_m > 0 else 0

    # --- 5. RELATIVE VALUATION ---
    # EPS = Net Income ($M) / Shares ($M)
    eps = inputs['net_income'] / shares_m if shares_m > 0 else 0
    price_pe = eps * 15  # Conservative 15x Multiple

    return {
        "df": df,
        "dcf_price": price_dcf,
        "pe_price": price_pe,
        "ev": ev_m,          # Total Value in $M
        "pv_terminal": pv_terminal,
        "current_price": inputs.get('current_price', 0),
        "ddm_price": 0       # Alphabet rarely pays high dividends; DCF is primary
    }


def calculate_sensitivity(inputs, growth_rate, wacc_range, g_range):
    """Generates an Enterprise Value matrix in Billions ($B)"""
    matrix = np.zeros((len(wacc_range), len(g_range)))
    # Placeholder market data for sensitivity consistency
    market_data = {'rf': 0.045, 'erp': 0.055}
    
    for i, w in enumerate(wacc_range):
        for j, g in enumerate(g_range):
            if w <= g:
                matrix[i, j] = np.nan
            else:
                res = run_multi_valuation(inputs, growth_rate, w, g, market_data)
                # Displaying in Billions ($B) for heatmap readability
                matrix[i, j] = res['ev'] / 1000
                
    return matrix
