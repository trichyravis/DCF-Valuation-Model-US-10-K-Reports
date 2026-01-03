def get_net_debt(xbrl: dict, extract) -> float:
    """
    Compute Net Debt = Total Debt - Cash & Cash Equivalents
    using latest 10-K data
    """

    # -------------------------------
    # CASH & CASH EQUIVALENTS
    # -------------------------------
    cash_df = extract(
        xbrl,
        tags=[
            "CashAndCashEquivalentsAtCarryingValue",
            "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"
        ],
        col_name="Cash"
    )

    cash = cash_df.iloc[0]["Cash"] if not cash_df.empty else 0.0

    # -------------------------------
    # TOTAL DEBT
    # -------------------------------
    short_debt_df = extract(
        xbrl,
        tags=["ShortTermBorrowings"],
        col_name="ShortDebt"
    )

    long_debt_df = extract(
        xbrl,
        tags=["LongTermDebt"],
        col_name="LongDebt"
    )

    short_debt = short_debt_df.iloc[0]["ShortDebt"] if not short_debt_df.empty else 0.0
    long_debt = long_debt_df.iloc[0]["LongDebt"] if not long_debt_df.empty else 0.0

    total_debt = short_debt + long_debt

    # -------------------------------
    # NET DEBT
    # -------------------------------
    net_debt = total_debt - cash

    return float(net_debt)

