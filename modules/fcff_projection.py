
import pandas as pd


def project_fcff(
    base_year: dict,
    growth_rates: list[float],
    sales_to_capital: float,
) -> pd.DataFrame:
    """
    Project FCFF over explicit forecast period using
    Damodaran-style reinvestment logic
    """

    revenue_0 = base_year["Revenue"]
    ebit_margin = base_year["EBIT"] / revenue_0 if revenue_0 > 0 else 0.0
    tax_rate = base_year["TaxRate"]

    rows = []

    revenue_prev = revenue_0

    for i, g in enumerate(growth_rates, start=1):
        revenue = revenue_prev * (1 + g)

        # Operating income
        ebit = revenue * ebit_margin
        nopat = ebit * (1 - tax_rate)

        # Reinvestment (Sales-to-Capital discipline)
        revenue_change = revenue - revenue_prev
        reinvestment = revenue_change / sales_to_capital if sales_to_capital > 0 else 0.0

        # FCFF
        fcff = nopat - reinvestment

        rows.append({
            "Year": i,
            "Revenue": revenue,
            "EBIT": ebit,
            "NOPAT": nopat,
            "Reinvestment": reinvestment,
            "FCFF": fcff
        })

        revenue_prev = revenue

    return pd.DataFrame(rows)
