
import pandas as pd


def project_fcff(
    base_revenue: float,
    operating_margin: float,
    tax_rate: float,
    growth_rates: list[float],
    sales_to_capital: float,
) -> pd.DataFrame:
    """
    Project FCFF over an explicit forecast period using
    Damodaran-style reinvestment logic.

    Parameters
    ----------
    base_revenue : float
        Latest audited revenue (from 10-K)
    operating_margin : float
        Base-year EBIT / Revenue
    tax_rate : float
        Effective tax rate
    growth_rates : list[float]
        Revenue growth assumptions (explicit years)
    sales_to_capital : float
        Revenue / Invested Capital (capital efficiency)
    """

    rows = []

    revenue_prev = base_revenue

    for year, g in enumerate(growth_rates, start=1):
        # Revenue forecast
        revenue = revenue_prev * (1 + g)

        # Operating income
        ebit = revenue * operating_margin
        nopat = ebit * (1 - tax_rate)

        # Reinvestment (growth-driven)
        revenue_change = revenue - revenue_prev
        reinvestment = (
            revenue_change / sales_to_capital
            if sales_to_capital > 0
            else 0.0
        )

        # FCFF
        fcff = nopat - reinvestment

        rows.append({
            "Year": year,
            "Revenue": revenue,
            "EBIT": ebit,
            "NOPAT": nopat,
            "Reinvestment": reinvestment,
            "FCFF": fcff,
        })

        revenue_prev = revenue

    return pd.DataFrame(rows)
