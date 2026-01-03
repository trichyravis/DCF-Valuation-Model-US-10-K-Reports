import numpy as np
import pandas as pd


def dcf_valuation(
    fcff_df: pd.DataFrame,
    wacc: float,
    terminal_growth: float,
    net_debt: float,
    shares_outstanding: float,
):
    """
    Perform DCF valuation using FCFF

    Parameters
    ----------
    fcff_df : DataFrame with columns ['Year', 'FCFF']
    wacc : float
    terminal_growth : float
    net_debt : float
    shares_outstanding : float
    """

    # -------------------------------
    # DISCOUNT EXPLICIT FCFF
    # -------------------------------
    fcff = fcff_df["FCFF"].values
    years = np.arange(1, len(fcff) + 1)

    discount_factors = (1 + wacc) ** years
    pv_fcff = fcff / discount_factors

    # -------------------------------
    # TERMINAL VALUE
    # -------------------------------
    terminal_fcff = fcff[-1] * (1 + terminal_growth)

    if wacc <= terminal_growth:
        raise ValueError("WACC must be greater than terminal growth rate")

    terminal_value = terminal_fcff / (wacc - terminal_growth)
    pv_terminal_value = terminal_value / discount_factors[-1]

    # -------------------------------
    # ENTERPRISE & EQUITY VALUE
    # -------------------------------
    enterprise_value = pv_fcff.sum() + pv_terminal_value
    equity_value = enterprise_value - net_debt

    fair_value_per_share = (
        equity_value / shares_outstanding
        if shares_outstanding > 0
        else np.nan
    )

    return {
        "EnterpriseValue": enterprise_value,
        "EquityValue": equity_value,
        "FairValuePerShare": fair_value_per_share,
        "PV_FCFF": pv_fcff,
        "PV_Terminal": pv_terminal_value,
    }

