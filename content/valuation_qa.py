VALUATION_QA = [
    ("1. What is Free Cash Flow to the Firm (FCFF)?", 
     "FCFF is the cash flow available to all capital providers (debt and equity) after all operating expenses, taxes, and necessary investments in working capital and fixed assets are paid."),
    
    ("2. Why use FCFF instead of Net Income for valuation?", 
     "Net Income includes non-cash items like depreciation and doesn't account for capital expenditures. FCFF represents the 'actual cash' that can be taken out of the business without harming its operations."),
    
    ("3. Where is the most reliable data found in a 10-K?", 
     "Item 8 (Financial Statements and Supplementary Data) contains the audited financial reports. Item 7 (MD&A) provides the management's context on why those numbers changed."),
    
    ("4. What is the 'Gordon Growth' Terminal Value?", 
     "It is a formula used to value the firm's cash flows beyond the 5-year forecast period. It assumes the firm grows at a constant rate ($g$) forever: $TV = [FCF_{n} \times (1+g)] / (WACC - g)$."),
    
    ("5. Why is the WACC used as the discount rate in FCFF?", 
     "Since FCFF belongs to both lenders and shareholders, the discount rate must reflect the weighted average cost of both debt and equity capital."),
    
    ("6. What does a high 'Sensitivity' to WACC indicate?", 
     "If the valuation drops significantly with a small increase in WACC, it indicates that much of the company's value is 'back-loaded' in the terminal value, often seen in high-growth tech companies."),
    
    ("7. How does 'Net Debt' impact the final share price?", 
     "We calculate Enterprise Value (EV) first. We then subtract Total Debt and add Cash (Net Debt) to arrive at the Equity Value, which is then divided by shares outstanding."),
    
    ("8. What is the 'Margin of Safety'?", 
     "It is the difference between the intrinsic value calculated by our DCF and the current market price. A 20-30% margin is often sought by value investors."),
    
    ("9. Why is Depreciation added back to EBIT?", 
     "Depreciation is a non-cash accounting expense. Since it didn't actually result in an outflow of cash this year, we add it back to see the true cash-generating power of the firm."),
    
    ("10. What is a 'Terminal Growth Rate' limit?", 
     "Mathematically, the terminal growth rate cannot exceed the long-term growth of the economy (usually 2-3%), or else the company would eventually become larger than the entire economy."),
    
    ("11. How does the 10-K treat CapEx?", 
     "Capital Expenditures are found in the Statement of Cash Flows. They represent long-term investments in PP&E that are essential for future growth but reduce current year cash flow."),
    
    ("12. What is 'Working Capital' in the DCF?", 
     "It represents the cash tied up in day-to-day operations (Inventory + Receivables - Payables). An increase in working capital is a cash outflow."),
    
    ("13. Explain the 'Two-Stage' model philosophy.", 
     "It acknowledges that companies cannot grow at high rates forever. The first stage captures high growth, while the second stage transitions to a stable, mature business model."),
    
    ("14. What are 'Non-GAAP' measures in a 10-K?", 
     "Companies often report 'Adjusted' numbers. Analysts must be careful as these often exclude 'real' costs like stock-based compensation to make earnings look better."),
    
    ("15. Why is the terminal value often 70%+ of the total value?", 
     "For most stable companies, the value of all future years (perpetuity) far outweighs the specific cash flows of the next five years, which is why the Terminal Growth assumption is so critical.")
]
