
ABOUT_CONTENT = {
    "intro": """
    This terminal utilizes a **Two-Stage Free Cash Flow to the Firm (FCFF)** model, the gold standard for institutional equity valuation. 
    By shifting from manual data entry to automated SEC retrieval, we minimize transcription risk and ensure 
    that our fundamental analysis is grounded in audited GAAP figures from Item 8 of the 10-K report.
    """,
    "workflow": """
    ### 🛠️ The Institutional Valuation Workflow
    1. **SEC Data Extraction:** Automated retrieval of Revenue, EBIT, and Debt from the most recent audited 10-K.
    2. **Stage 1 (High Growth):** A 5-year explicit forecast period where the firm is expected to grow at an above-market rate.
    3. **Stage 2 (Stable Growth):** Calculation of Terminal Value using the Gordon Growth Method, assuming the firm reaches steady-state.
    4. **Intrinsic Value Calculation:** Discounting all future cash flows by the **WACC** and adjusting for Net Debt to reach Equity Value.
    """,
    "arima": """
    **Stage 1 Assumption:** We assume a 'Fade' in growth rates from the initial input toward the terminal rate over 5 years.
    """,
    "vasicek": """
    **WACC Assumption:** The discount rate represents the opportunity cost of all capital providers, reflecting the firm's specific risk profile.
    """,
    "cir": """
    **Terminal Assumption:** We assume a long-term growth rate ($g$) that does not exceed the risk-free rate, ensuring the model remains economically grounded.
    """
}
