
import numpy as np
import pandas as pd


def dcf_valuation(
    fcff_projection: pd.DataFrame,
    wacc: float,
    terminal_growth: float,
    net_debt: float = 0.0,
    shares_outstanding: float = 1.0,
):
    """
    Perform DCF valuation using projected FCFF

    Parameters
    ----------
    fcff_projection : DataFrame
        Must contain columns ['Year', 'FCFF']
    wacc : float
    terminal_growth : float
    net_debt : float
    shares_outstanding : float
    """

    fcff = fcff_projection["FCFF"].values
    years = np.arange(1, len(fcff) + 1)

    # -------------------------------
    # Discount FCFF
    # -------------------------------
    discount_factors = (1 + wacc) ** years
    pv_fcff = fcff / discount_factors

    # -------------------------------
    # Terminal Value
    # -------------------------------
    if wacc <= terminal_growth:
        raise ValueError("WACC must be greater than terminal growth rate")

    terminal_fcff = fcff[-1] * (1 + terminal_growth)
    terminal_value = terminal_fcff / (wacc - terminal_growth)
    pv_terminal_value = terminal_value / discount_factors[-1]

    # -------------------------------
    # Valuation
    # -------------------------------
    enterprise_value = pv_fcff.sum() + pv_terminal_value
    equity_value = enterprise_value - net_debt
    fair_value_per_share = equity_value / shares_outstanding

    return {
        "EnterpriseValue": enterprise_value,
        "EquityValue": equity_value,
        "FairValuePerShare": fair_value_per_share,
        "PV_FCFF": pv_fcff,
        "PV_Terminal": pv_terminal_value,
    }
