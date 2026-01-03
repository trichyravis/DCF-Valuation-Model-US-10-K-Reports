import pandas as pd


def get_base_year_operating_data(xbrl: dict, extract) -> dict:
    """
    Extract base-year (latest 10-K) operating inputs required for FCFF valuation
    """

    # -------------------------------
    # Revenue
    # -------------------------------
    revenue_df = extract(
        xbrl,
        tags=["Revenues", "SalesRevenueNet"],
        col_name="Revenue"
    )

    # -------------------------------
    # EBIT (Operating Income)
    # -------------------------------
    ebit_df = extract(
        xbrl,
        tags=["OperatingIncomeLoss"],
        col_name="EBIT"
    )

    # -------------------------------
    # Income Before Tax
    # -------------------------------
    pbt_df = extract(
        xbrl,
        tags=[
            "IncomeBeforeTax",
            "IncomeLossFromContinuingOperationsBeforeIncomeTaxes"
        ],
        col_name="PBT"
    )

    # -------------------------------
    # Income Tax
    # -------------------------------
    tax_df = extract(
        xbrl,
        tags=["IncomeTaxExpenseBenefit"],
        col_name="Tax"
    )

    # -------------------------------
    # Depreciation & Amortization
    # -------------------------------
    dep_df = extract(
        xbrl,
        tags=["DepreciationAndAmortization"],
        col_name="Dep"
    )

    # -------------------------------
    # CapEx
    # -------------------------------
    capex_df = extract(
        xbrl,
        tags=["PaymentsToAcquirePropertyPlantAndEquipment"],
        col_name="CapEx"
    )

    # -------------------------------
    # VALIDATION
    # -------------------------------
    if revenue_df.empty or ebit_df.empty:
        raise ValueError("Insufficient 10-K data to extract base year")

    # Use latest fiscal year only
    year = revenue_df.iloc[0]["Year"]

    revenue = revenue_df.iloc[0]["Revenue"]
    ebit = ebit_df.iloc[0]["EBIT"]

    tax_rate = 0.21  # conservative default

    if not pbt_df.empty and not tax_df.empty:
        pbt = pbt_df.iloc[0]["PBT"]
        tax = tax_df.iloc[0]["Tax"]
        if pbt > 0:
            tax_rate = min(max(tax / pbt, 0.10), 0.30)

    depreciation = dep_df.iloc[0]["Dep"] if not dep_df.empty else 0.0
    capex = abs(capex_df.iloc[0]["CapEx"]) if not capex_df.empty else 0.0

    # -------------------------------
    # RETURN CLEAN BASE-YEAR DATA
    # -------------------------------
    return {
        "year": int(year),
        "revenue": float(revenue),
        "ebit": float(ebit),
        "operating_margin": float(ebit / revenue),
        "tax_rate": float(tax_rate),
        "depreciation": float(depreciation),
        "capex": float(capex),
    }
