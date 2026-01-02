
import pandas as pd
import streamlit as st
import requests

class SECDataFetcher:
    def __init__(self, ticker):
        self.ticker = ticker
        self.headers = {
            'User-Agent': 'Mountain Path Valuation (your-email@example.com)',
            'Accept-Encoding': 'gzip, deflate'
        }

    @st.cache_data(ttl=3600)
    def get_valuation_inputs(_self):
        try:
            # 1. Map Ticker to CIK
            ticker_map = requests.get("https://www.sec.gov/files/company_tickers.json", headers=_self.headers).json()
            cik = next((str(item['cik_str']).zfill(10) for item in ticker_map.values() if item['ticker'] == _self.ticker.upper()), None)
            
            if not cik: return None

            # 2. Fetch Facts
            facts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=_self.headers).json()
            
            def get_val(tag, taxonomy='us-gaap'):
                try:
                    data = facts['facts'][taxonomy][tag]['units']['USD']
                    return sorted(data, key=lambda x: x['end'])[-1]['val']
                except: return 0

            # 3. Pull all requirements for your Pfizer-style model
            return {
                "name": _self.ticker,
                "revenue": get_val('Revenues') / 1e6,
                "ebit": get_val('OperatingIncomeLoss') / 1e6,
                "net_income": get_val('NetIncomeLoss') / 1e6,
                "depr": get_val('DepreciationDepletionAndAmortization') / 1e6,
                "capex": get_val('PaymentsToAcquirePropertyPlantAndEquipment') / 1e6,
                "debt": (get_val('LongTermDebtNoncurrent') + get_val('DebtCurrent')) / 1e6,
                "cash": get_val('CashAndCashEquivalentsAtCarryingValue') / 1e6,
                "interest_exp": get_val('InterestExpense') / 1e6,
                "dividends": get_val('PaymentsOfDividends') / 1e6,
                "shares": get_val('EntityCommonStockSharesOutstanding', 'dei') or 1e6,
                "tax_rate": 0.21 # Default corporate tax
            }
        except Exception as e:
            st.error(f"SEC Fetch Error: {e}")
            return None
