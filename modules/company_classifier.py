def classify_company(xbrl, extract):
    """
    Classify company based on SEC XBRL characteristics.
    Returns: 'Financial' or 'Non-Financial'
    """
    interest_income = extract(
        xbrl,
        ["InterestIncome"],
        "InterestIncome"
    )

    if not interest_income.empty:
        return "Financial"

    return "Non-Financial"

