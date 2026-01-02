
import yfinance as yf
import pandas as pd
import streamlit as st

class SECDataFetcher:
    def __init__(self, ticker):
        self.ticker = ticker
        # Adding a session with headers helps prevent "Too Many Requests" errors
        self.stock = yf.Ticker(ticker)

    def get_valuation_inputs(self):
        """Fetches audited 10-K financial data and standardizes to Millions ($M)"""
        try:
            # yfinance pulls the 'financials' table which maps to the 10-K
            # We use .annuals to ensure we aren't picking up 10-Q (quarterly) data
            income = self.stock.get_financials(freq='annual')
            bs = self.stock.get_balance_sheet(freq='annual')
            cf = self.stock.get_cashflow(freq='annual')
            info = self.stock.info
            
            if income.empty or bs.empty:
                return None

            def get_val(df, labels):
                for label in labels:
                    if label in df.index:
                        val = df.loc[label].iloc[0]
                        return val if pd.notnull(val) else 0
                return 0

            # 10-K Extraction (Values in Millions)
            revenue = get_val(income, ['Total Revenue', 'Operating Revenue']) / 1e6
            ebit = get_val(income, ['EBIT', 'Operating Income']) / 1e6
            tax_exp = get_val(income, ['Tax Provision', 'Income Tax Expense']) / 1e6
            
            # Balance Sheet (Latest Audited Year)
            total_debt = get_val(bs, ['Total Debt', 'Long Term Debt']) / 1e6
            cash = get_val(bs, ['Cash And Cash Equivalents', 'Cash Cash Equivalents And Short Term Investments']) / 1e6
            
            # Cash Flow
            capex = abs(get_val(cf, ['Capital Expenditure', 'Net PPE Purchase And Sale'])) / 1e6
            depr = get_val(cf, ['Depreciation And Amortization', 'Depreciation']) / 1e6

            return {
                "name": info.get('longName', self.ticker),
                "revenue": revenue,
                "ebit": ebit,
                "tax_rate": abs(tax_exp / ebit) if ebit != 0 else 0.21,
                "capex": capex,
                "depr": depr,
                "debt": total_debt,
                "cash": cash,
                "shares": info.get('sharesOutstanding', 1)
            }
        except Exception as e:
            st.error(f"SEC Data Error: {str(e)}")
            return None
