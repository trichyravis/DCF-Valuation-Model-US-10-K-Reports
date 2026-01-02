
import pandas as pd
import streamlit as st
import requests
import yfinance as yf
import time

class SECDataFetcher:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        # SEC requires a specific User-Agent format: Company Name/Email
        self.headers = {
            'User-Agent': 'Mountain Path Valuation (research@mountainpath.edu)',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'data.sec.gov'
        }

    @st.cache_data(ttl=3600)
    def get_valuation_inputs(_self):
        try:
            # 1. Map Ticker to CIK
            ticker_map = requests.get("https://www.sec.gov/files/company_tickers.json", 
                                     headers={'User-Agent': 'MPV/1.0'}).json()
            cik = next((str(item['cik_str']).zfill(10) for item in ticker_map.values() 
                       if item['ticker'] == _self.ticker), None)
            
            if not cik: return None

            # 2. Fetch Audited Facts
            facts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", 
                                headers=_self.headers).json()
            
            def get_val(tag, taxonomy='us-gaap'):
                try:
                    data = facts['facts'][taxonomy][tag]['units']['USD']
                    return sorted(data, key=lambda x: x['end'])[-1]['val']
                except: return 0

            # 3. Live Price Fallback
            stock = yf.Ticker(_self.ticker)
            try:
                current_price = stock.fast_info['last_price']
            except:
                hist = stock.history(period="1d")
                current_price = hist['Close'].iloc[-1] if not hist.empty else 0

            return {
                "name": _self.ticker,
                "ticker": _self.ticker,
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
            st.error(f"SEC Fetch Error: {e}")
            return None
