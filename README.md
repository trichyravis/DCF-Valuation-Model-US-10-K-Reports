# THE MOUNTAIN PATH - WORLD OF FINANCE
## Dynamic Nifty Stock Relative Valuation Model

**Prof. V. Ravichandran**  
28+ Years Corporate Finance & Banking Experience  
10+ Years Academic Excellence

---

## 📊 PROJECT OVERVIEW

A comprehensive **Streamlit-based Stock Analysis Platform** for analyzing Indian Nifty 50 stocks using advanced relative valuation methodologies. This application provides institutional-grade financial analysis with a professional, educational interface.

### Key Features

#### 1. **Single Stock Analysis**
- Real-time stock data fetching
- Comprehensive relative valuation metrics
- Technical analysis with moving averages
- Price trend visualization
- Valuation signal generation

#### 2. **Sector Comparison**
- Sector-wise stock analysis
- Comparative valuation multiples
- Sector performance metrics
- Peer benchmarking

#### 3. **Multi-Stock Comparison**
- Compare up to 6 stocks simultaneously
- Radar charts for multi-dimensional analysis
- Relative performance metrics
- Cross-stock valuation comparison

#### 4. **Relative Valuation Matrix**
- Comprehensive Nifty 50 analysis
- Sector-wise summary statistics
- Heatmap visualization of multiples
- Distribution analysis by sector

---

## 📈 RELATIVE VALUATION FRAMEWORK

### Core Valuation Multiples

#### **1. Price-to-Earnings Ratio (P/E)**
```
P/E = Current Stock Price / Earnings Per Share

Interpretation:
- P/E < 12: Potentially Undervalued
- P/E 12-18: Fair Value
- P/E > 25: Potentially Overvalued

Use Case: Most commonly used valuation metric
Advantage: Simple, widely understood
Limitation: Affected by accounting policies, cyclical earnings
```

#### **2. Price-to-Book Ratio (P/B)**
```
P/B = Current Stock Price / Book Value Per Share

Interpretation:
- P/B < 1: Trading below book value (value play)
- P/B 1-3: Fair value range
- P/B > 3: Potentially overvalued

Use Case: Particularly useful for capital-intensive industries
Advantage: Based on tangible asset value
Limitation: Book value may not reflect true economic value
```

#### **3. Price-to-Sales Ratio (P/S)**
```
P/S = Market Cap / Total Revenue

Interpretation:
- P/S < 1: Undervalued
- P/S 1-3: Fair value
- P/S > 3: Potentially overvalued

Use Case: Useful for companies with negative earnings
Advantage: Less susceptible to accounting manipulation
Limitation: Doesn't account for profitability differences
```

#### **4. Enterprise Value / EBITDA**
```
EV = Market Cap + Debt - Cash
EV/EBITDA = Enterprise Value / EBITDA

Interpretation:
- EV/EBITDA < 8: Potentially undervalued
- EV/EBITDA 8-12: Fair value
- EV/EBITDA > 15: Potentially overvalued

Use Case: Capital structure neutral valuation
Advantage: Comparable across companies with different capital structures
Limitation: Requires access to EBITDA data
```

#### **5. PEG Ratio (Price/Earnings to Growth)**
```
PEG = P/E Ratio / Earnings Growth Rate (%)

Interpretation:
- PEG < 1: Undervalued relative to growth
- PEG = 1: Fair valuation
- PEG > 1: Overvalued relative to growth

Use Case: Best for high-growth companies
Advantage: Accounts for expected growth
Limitation: Sensitive to growth rate estimates
```

#### **6. Dividend Yield**
```
Dividend Yield = Annual Dividends Per Share / Current Price

Use Case: Income-focused investors
Interpretation:
- High dividend yield: Attractive for income
- Growth vs. Yield tradeoff important
```

---

## 🚀 INSTALLATION & SETUP

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone/Download Project
```bash
# Create project directory
mkdir nifty-valuation-model
cd nifty-valuation-model
```

### Step 2: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
# Check if streamlit is installed
streamlit --version
```

### Step 4: Run Application
```bash
# Launch the Streamlit app
streamlit run nifty_valuation_model.py
```

The application will open in your default browser at `http://localhost:8501`

---

## 📋 USAGE GUIDE

### Navigation

#### **Single Stock Analysis**
1. Select stock from dropdown
2. View comprehensive metrics:
   - Company information
   - Current price and market cap
   - Valuation multiples (P/E, P/B, P/S, EV/EBITDA)
   - Performance metrics (dividend yield, earnings growth)
   - Valuation signals
3. View price chart with technical analysis
   - 20-day moving average
   - 50-day moving average
   - Historical trend

#### **Sector Comparison**
1. Select sector from dropdown
2. View all companies in sector
3. Compare valuation metrics
4. Analyze sector averages:
   - Average P/E, P/B, P/S
   - Average Dividend Yield
5. Visualize distributions

#### **Multi-Stock Comparison**
1. Select up to 6 stocks
2. View comparative table
3. Analyze multi-dimensional comparison using radar chart
4. Identify relative valuations

#### **Relative Valuation Matrix**
1. Select sectors for analysis
2. View comprehensive matrix
3. Analyze sector summaries
4. Study distribution patterns

---

## 💻 ADVANCED FINANCIAL RISK MODELING

The `financial_risk_modeling.py` module provides advanced calculations:

### 1. **RelativeValuation Class**
Complete relative valuation analysis with valuation scoring

```python
from financial_risk_modeling import RelativeValuation

company_data = {
    'current_price': 2500,
    'earnings_per_share': 150,
    'book_value_per_share': 400,
    'sales_per_share': 1000,
    'ebitda': 50000,
    'revenue': 500000,
    'market_cap': 500000,
    'debt': 100000,
    'cash': 50000,
    'dividends_per_share': 50,
    'earnings_growth_rate': 15
}

val_model = RelativeValuation(company_data)
metrics = val_model.calculate_all_metrics()
score = val_model.get_valuation_score()
```

### 2. **FinancialRiskModel Class**
Comprehensive risk analysis

```python
from financial_risk_modeling import FinancialRiskModel

# Historical returns data
returns = [0.02, -0.01, 0.03, 0.01, -0.02, 0.04, ...]

risk_model = FinancialRiskModel(returns)
risk_metrics = risk_model.calculate_all_risk_metrics()

# Metrics calculated:
# - Value at Risk (VAR)
# - Conditional Value at Risk (CVaR)
# - Sharpe Ratio
# - Sortino Ratio
# - Maximum Drawdown
# - Volatility
# - Beta (if market returns provided)
```

### 3. **SectorValuationAnalysis Class**
Sector-level comparative analysis

```python
from financial_risk_modeling import SectorValuationAnalysis

sector_analysis = SectorValuationAnalysis(sector_data)
sector_metrics = sector_analysis.calculate_sector_metrics()
ranked_sectors = sector_analysis.rank_sectors_by_valuation()
```

### 4. **FinancialHealthAnalysis Class**
Leverage and solvency metrics

```python
from financial_risk_modeling import FinancialHealthAnalysis

health_analysis = FinancialHealthAnalysis(financial_data)
health_metrics = health_analysis.calculate_all_metrics()
health_score = health_analysis.calculate_financial_health_score()
```

### 5. **PortfolioAnalysis Class**
Portfolio-level metrics

```python
from financial_risk_modeling import PortfolioAnalysis

portfolio = PortfolioAnalysis(holdings, weights)
portfolio_metrics = portfolio.calculate_all_portfolio_metrics()
```

---

## 📊 FINANCIAL METRICS INTERPRETATION

### Risk Assessment Framework

#### **Value at Risk (VAR)**
- Definition: Maximum expected loss with given confidence level
- VAR(95%) = Worst expected return 95% of the time
- Used for: Risk budgeting, position sizing

#### **Sharpe Ratio**
- Formula: (Average Return - Risk-Free Rate) / Volatility
- Interpretation:
  - > 1.0: Good risk-adjusted return
  - > 1.5: Very good
  - > 2.0: Excellent
- Used for: Comparing risk-adjusted performance

#### **Sortino Ratio**
- Formula: (Average Return - Target) / Downside Deviation
- Better than Sharpe for downside risk focus
- Used for: Conservative investors concerned with losses

#### **Maximum Drawdown**
- Definition: Largest peak-to-trough decline
- Interpretation: Maximum loss experienced historically
- Used for: Understanding worst-case scenarios

#### **Beta**
- Definition: Systematic risk relative to market
- Beta > 1: More volatile than market
- Beta = 1: Moves with market
- Beta < 1: Less volatile than market
- Used for: Portfolio risk assessment

---

## 🎯 VALUATION SIGNALS

The platform generates signals based on comprehensive analysis:

### **Undervaluation Signals**
- P/E < 12
- P/B < 1
- P/S < 1
- EV/EBITDA < 8
- PEG < 1
- High Dividend Yield

### **Overvaluation Signals**
- P/E > 25
- P/B > 3
- P/S > 3
- EV/EBITDA > 15
- PEG > 1.5

### **Fair Value Signals**
- Multiples within normal ranges
- Growth and valuation aligned

---

## 📁 PROJECT STRUCTURE

```
nifty-valuation-model/
├── nifty_valuation_model.py          # Main Streamlit application
├── financial_risk_modeling.py         # Financial modeling classes
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

### File Descriptions

#### `nifty_valuation_model.py`
- Main Streamlit application
- User interface and visualizations
- Data fetching and processing
- Multiple analysis modes

#### `financial_risk_modeling.py`
- Relative valuation calculations
- Financial risk models
- Sector analysis
- Financial health metrics
- Portfolio analysis tools

#### `requirements.txt`
- All required Python packages
- Version specifications

---

## 🔧 CUSTOMIZATION

### Adding New Stocks

Edit the `NIFTY_50_DATA` dictionary in `nifty_valuation_model.py`:

```python
NIFTY_50_DATA = {
    'SYMBOL.NS': {'Company': 'Company Name', 'Sector': 'Sector Name'},
    # Add more stocks here
}
```

### Modifying Valuation Thresholds

Adjust thresholds in the `get_valuation_signal()` function:

```python
def get_valuation_signal(pe, pb, ps):
    signals = []
    
    if pe and pe < 12:  # Modify this threshold
        signals.append("Undervalued (P/E)")
    # ... rest of function
```

### Customizing Analysis Periods

Modify period options in sidebar:

```python
period = st.selectbox(
    "Select Time Period:",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"],  # Add/remove periods
)
```

---

## 📈 NIFTY 50 STOCKS COVERED

### IT & Software (6 stocks)
- TCS, Infosys, Wipro, HCL Tech, Tech Mahindra, LT Tech Services

### Financial Services (8 stocks)
- HDFC Bank, ICICI Bank, Axis Bank, Bajaj Finserv, SBI, SBILIFE, HDFCLIFE, IndusInd

### Energy & Utilities (6 stocks)
- Reliance, NTPC, Power Grid, IOCL, Gail, ONGC

### Consumer & FMCG (8 stocks)
- Hindustan Unilever, Titan, Nestlé India, Asian Paints, Marico, Bajaj Electricals, Britannia, Procter & Gamble

### Metals & Mining (3 stocks)
- Tata Steel, JSW Steel, Coal India

### Automobiles (4 stocks)
- Maruti, Hero MotoCorp, Bajaj Auto, Mahindra & Mahindra

### Pharmaceuticals (5 stocks)
- Sun Pharma, Divi Lab, Cipla, Dr Reddy Labs, Biocon

### Infrastructure & Construction (3 stocks)
- Larsen & Toubro, Adani Ports, UltraCem

### Telecom (1 stock)
- Bharti Airtel

### Healthcare (1 stock)
- Apollo Hospitals

### Holding Companies (1 stock)
- Bajaj Holdings

---

## 🔐 DATA SOURCES

- **Stock Data**: Yahoo Finance (via yfinance)
- **Real-time Updates**: Every hour (configurable)
- **Historical Data**: Last 5 years available

---

## ⚠️ DISCLAIMER

This tool is for **educational purposes only**. It provides financial analysis frameworks and methodologies taught in MBA and CFA curricula.

**Important:**
- This is NOT investment advice
- Past performance does not guarantee future results
- Always conduct your own due diligence
- Consult with financial advisors before making investment decisions
- Use at your own risk

---

## 🎓 EDUCATIONAL FRAMEWORK

This application teaches:

1. **Relative Valuation Principles**
   - Comparable company analysis
   - Multiples-based valuation
   - Peer benchmarking

2. **Financial Risk Assessment**
   - Quantitative risk metrics
   - Portfolio risk analysis
   - Sector risk comparison

3. **Financial Analysis**
   - Leverage analysis
   - Liquidity assessment
   - Cash flow analysis

4. **Data Visualization**
   - Interactive charts
   - Comparative analysis
   - Trend analysis

---

## 📞 SUPPORT & RESOURCES

### Additional Learning Resources

**Relative Valuation:**
- "Valuation: Measuring and Managing the Value of Companies" - Damodaran
- CFA Level 2 & 3 curriculum

**Financial Risk:**
- "Risk Management and Financial Institutions" - Hull
- Basel III regulatory frameworks

**Python Finance:**
- Official yfinance documentation
- Plotly visualization guide
- Streamlit documentation

---

## 🔄 VERSION HISTORY

### Version 1.0 (Current)
- Launch of core platform
- Relative valuation analysis
- Sector comparison tools
- Multi-stock analysis
- Risk metrics integration

### Planned Features
- Advanced scenario analysis
- Portfolio optimization
- Machine learning valuation models
- Real-time alerts
- Custom watchlists

---

## 📝 NOTES FOR DEVELOPERS

### Code Quality
- Type hints recommended
- Docstrings included
- Error handling implemented
- Caching for performance

### Performance Optimization
- Data caching with 1-hour TTL
- Vectorized calculations
- Efficient data structures

### Testing Recommendations
- Test with various market conditions
- Verify calculations against manual examples
- Test sector filtering logic

---

## 🤝 CONTRIBUTION GUIDELINES

To extend this framework:

1. Add new financial metrics in `financial_risk_modeling.py`
2. Create new analysis modes in Streamlit app
3. Implement additional visualizations
4. Enhance sector classifications

---

## 📚 TEACHING NOTES

### MBA Curriculum Integration

**Modules:**
- Financial Analysis & Valuation
- Risk Management
- Investment Banking
- Corporate Finance

**Topics Covered:**
- Equity valuation methodologies
- Market multiples analysis
- Risk-return tradeoffs
- Financial leverage
- Sector analysis

### CFA Preparation

**Study Areas:**
- Relative valuation methods
- Equity analysis frameworks
- Risk quantification
- Portfolio management

---

## 🏆 BEST PRACTICES

### For Analysis
1. Always use multiple valuation metrics
2. Compare to sector and market averages
3. Consider growth rates (PEG analysis)
4. Assess financial health separately
5. Use peer comparison context

### For Interpretation
1. No single metric tells complete story
2. Consider industry dynamics
3. Evaluate management quality
4. Assess competitive positioning
5. Account for macroeconomic factors

---

## 📧 CONTACT & FEEDBACK

**Prof. V. Ravichandran**
- 28+ Years Corporate Finance & Banking Experience
- 10+ Years Academic Excellence
- Educational Platform: "The Mountain Path - World of Finance"

---

**Last Updated:** December 2025

---

## License

Educational and academic use permitted. Commercial licensing available upon request.

---

**Happy Analyzing! 📊💰**

*The Mountain Path - World of Finance*
