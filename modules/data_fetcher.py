
import pandas as pd
import streamlit as st
import requests
import yfinance as yf
import time

class SECDataFetcher:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        # SEC MANDATORY: Professional User-Agent with contact email
        self.headers = {
            'User-Agent': 'Mountain Path Valuation research@mountainpath.edu',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'data.sec.gov'
        }

    @st.cache_data(ttl=3600)
    def get_valuation_inputs(_self):
        try:
            # Step 1: Map Ticker to CIK
            ticker_map_url = "https://www.sec.gov/files/company_tickers.json"
            map_headers = {'User-Agent': 'MPV research@mountainpath.edu'}
            response = requests.get(ticker_map_url, headers=map_headers)
            
            if not response.text.strip(): return None
            ticker_map = response.json()
            
            # --- FIXING THE NAMEERROR: Initialize cik before use ---
            cik = None 
            for item in ticker_map.values():
                if item['ticker'] == _self.ticker:
                    cik = str(item['cik_str']).zfill(10)
                    break
            
            if not cik:
                st.error(f"Ticker {_self.ticker} not found in SEC database.")
                return None

            # Step 2: Fetch Audited Facts
            facts_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
            facts_res = requests.get(facts_url, headers=_self.headers)
            if not facts_res.text.strip(): return None
            facts = facts_res.json()
            
            def get_val(tag, taxonomy='us-gaap'):
                try:
                    data = facts['facts'][taxonomy][tag]['units']['USD']
                    return sorted(data, key=lambda x: x['end'])[-1]['val']
                except: return 0

            # Step 3: Fetch Market Price
            stock = yf.Ticker(_self.ticker)
            try:
                current_price = stock.fast_info['last_price']
            except:
                hist = stock.history(period="1d")
                current_price = hist['Close'].iloc[-1] if not hist.empty else 0

            return {
                "name": _self.ticker,
                "current_price": current_price,
                "revenue": get_val('Revenues') / 1e6 or get_val('RevenueFromContractWithCustomerExcludingCostReportedAmount') / 1e6,
                "ebit": get_val('OperatingIncomeLoss') / 1e6,
                "net_income": get_val('NetIncomeLoss') / 1e6,
                "depr": get_val('DepreciationDepletionAndAmortization') / 1e6,
                "capex": get_val('PaymentsToAcquirePropertyPlantAndEquipment') / 1e6,
                "debt": (get_val('LongTermDebtNoncurrent') + get_val('DebtCurrent')) / 1e6,
                "cash": get_val('CashAndCashEquivalentsAtCarryingValue') / 1e6,
                "interest_exp": get_val('InterestExpense') / 1e6,
                "dividends": get_val('PaymentsOfDividends') / 1e6,
                "shares": get_val('EntityCommonStockSharesOutstanding', 'dei') or 1e6,
                "tax_rate": 0.21,
                "beta": 1.1
            }
        except Exception as e:
            st.error(f"Fetch Error: {e}")
            return None
