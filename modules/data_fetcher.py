
import pandas as pd
import streamlit as st
import requests
import yfinance as yf

class SECDataFetcher:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.headers = {
            'User-Agent': 'Mountain Path Valuation (your-email@example.com)',
            'Accept-Encoding': 'gzip, deflate'
        }

    @st.cache_data(ttl=3600)
    def get_valuation_inputs(_self):
        """Fetches audited SEC data and real-time market price"""
        try:
            # 1. Map Ticker to CIK via SEC
            ticker_map = requests.get("https://www.sec.gov/files/company_tickers.json", headers=_self.headers).json()
            cik = next((str(item['cik_str']).zfill(10) for item in ticker_map.values() if item['ticker'] == _self.ticker), None)
            
            if not cik:
                return None

            # 2. Fetch Audited Facts from SEC EDGAR
            facts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=_self.headers).json()
            
            def get_sec_val(tag, taxonomy='us-gaap'):
                try:
                    data = facts['facts'][taxonomy][tag]['units']['USD']
                    return sorted(data, key=lambda x: x['end'])[-1]['val']
                except: return 0

            # 3. Fetch Real-time Market Price via yfinance
            # We use fast_info for speed or history for the latest 'Close'
            stock = yf.Ticker(_self.ticker)
            current_price = stock.fast_info['last_price'] if 'last_price' in stock.fast_info else 0
            
            if current_price == 0:
                # Fallback to history if fast_info fails
                hist = stock.history(period="1d")
                current_price = hist['Close'].iloc[-1] if not hist.empty else 0

            # 4. Consolidate Data
            return {
                "name": _self.ticker,
                "current_price": current_price,
                "revenue": get_sec_val('Revenues') / 1e6,
                "ebit": get_sec_val('OperatingIncomeLoss') / 1e6,
                "net_income": get_sec_val('NetIncomeLoss') / 1e6,
                "depr": get_sec_val('DepreciationDepletionAndAmortization') / 1e6,
                "capex": get_sec_val('PaymentsToAcquirePropertyPlantAndEquipment') / 1e6,
                "debt": (get_sec_val('LongTermDebtNoncurrent') + get_sec_val('DebtCurrent')) / 1e6,
                "cash": get_sec_val('CashAndCashEquivalentsAtCarryingValue') / 1e6,
                "interest_exp": get_sec_val('InterestExpense') / 1e6,
                "dividends": get_sec_val('PaymentsOfDividends') / 1e6,
                "shares": get_sec_val('EntityCommonStockSharesOutstanding', 'dei') or 1e6,
                "tax_rate": 0.21
            }
        except Exception as e:
            st.error(f"Hybrid Data Fetch Error: {e}")
            return None
