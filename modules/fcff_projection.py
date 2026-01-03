
import pandas as pd


def project_fcff(
    base_revenue: float,
    operating_margin: float,
    tax_rate: float,
    growth_rates: list,
    sales_to_capital: float,
) -> pd.DataFrame:
    """
    Project FCFF using Damodaran-style reinvestment logic
    """

    results = []
    revenue_prev = base_revenue

    for year, g in enumerate(growth_rates, start=1):
        revenue = revenue_prev * (1 + g)

        ebit = revenue * operating_margin
        nopat = ebit * (1 - tax_rate)

        revenue_change = revenue - revenue_prev
        reinvestment = (
            revenue_change / sales_to_capital
            if sales_to_capital > 0
            else 0.0
        )

        fcff = nopat - reinvestment

        results.append({
            "Year": year,
            "Revenue": revenue,
            "EBIT": ebit,
            "NOPAT": nopat,
            "Reinvestment": reinvestment,
            "FCFF": fcff,
        })

        revenue_prev = revenue

    return pd.DataFrame(results)
