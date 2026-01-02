
import streamlit as st
import requests
import yfinance as yf
import json


class SECDataFetcher:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
    
    def get_valuation_inputs(self):
        try:
            # Step 1: Get ticker to CIK mapping
            ticker_map_url = "https://www.sec.gov/files/company_tickers.json"
            headers = {'User-Agent': 'Mountain Path Valuation (research@mountainpath.edu)'}
            
            try:
                response = requests.get(ticker_map_url, headers=headers, timeout=10)
                response.raise_for_status()
                ticker_map = response.json()
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to fetch ticker mapping from SEC: {e}")
                return None
            
            # Step 2: Find CIK for this ticker
            cik = None
            for item in ticker_map.values():
                if item.get('ticker') == self.ticker:
                    cik = str(item.get('cik_str', '')).zfill(10)
                    break
            
            if not cik or cik == '0000000000':
                st.error(f"Ticker {self.ticker} not found in SEC database")
                return None
            
            # Step 3: Fetch company facts from SEC
            facts_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
            
            try:
                facts_response = requests.get(facts_url, headers=headers, timeout=10)
                facts_response.raise_for_status()
                facts = facts_response.json()
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to fetch SEC data for {self.ticker}: {e}")
                return None
            except json.JSONDecodeError as e:
                st.error(f"Invalid response from SEC API: {e}")
                return None
            
            # Step 4: Extract financial values
            def get_val(tag, taxonomy='us-gaap'):
                try:
                    data = facts.get('facts', {}).get(taxonomy, {}).get(tag, {}).get('units', {}).get('USD', [])
                    if data:
                        return sorted(data, key=lambda x: x.get('end', ''))[-1].get('val', 0)
                    return 0
                except:
                    return 0
            
            # Step 5: Get current market price
            try:
                stock = yf.Ticker(self.ticker)
                hist = stock.history(period="1d")
                current_price = float(hist['Close'].iloc[-1]) if not hist.empty else 0
            except:
                current_price = 0
            
            # Return all financial metrics
            return {
                "name": self.ticker,
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
            st.error(f"Unexpected error: {str(e)}")
            return None
