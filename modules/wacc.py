import yfinance as yf


def calculate_wacc(
    ticker: str,
    risk_free_rate: float = 0.045,
    equity_risk_premium: float = 0.055,
    cost_of_debt: float = 0.04,
    tax_rate: float = 0.21,
):
    """
    Calculate WACC using CAPM for cost of equity.

    Parameters
    ----------
    ticker : str
        Stock ticker
    risk_free_rate : float
        Proxy for US 10Y Treasury
    equity_risk_premium : float
        Market risk premium
    cost_of_debt : float
        Pre-tax cost of debt
    tax_rate : float
        Corporate tax rate
    """

    stock = yf.Ticker(ticker)

    info = stock.info or {}

    beta = info.get("beta", 1.0)
    market_cap = info.get("marketCap", None)

    if market_cap is None:
        raise ValueError("Market cap not available from Yahoo Finance")

    # Capital structure weights
    equity_value = market_cap
    debt_value = 0.0  # Conservative default (net debt handled separately)

    total_value = equity_value + debt_value

    equity_weight = equity_value / total_value
    debt_weight = debt_value / total_value

    # Cost of equity (CAPM)
    cost_of_equity = risk_free_rate + beta * equity_risk_premium

    # WACC
    wacc = (
        equity_weight * cost_of_equity
        + debt_weight * cost_of_debt * (1 - tax_rate)
    )

    return {
        "WACC": wacc,
        "CostOfEquity": cost_of_equity,
        "Beta": beta,
        "EquityWeight": equity_weight,
        "DebtWeight": debt_weight,
    }

