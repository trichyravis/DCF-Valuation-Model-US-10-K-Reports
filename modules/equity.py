def get_share_count(xbrl: dict, extract) -> float:
    """
    Extract diluted shares outstanding from the latest 10-K
    """

    # ----------------------------------
    # PRIMARY: Diluted Shares
    # ----------------------------------
    diluted_df = extract(
        xbrl,
        tags=[
            "WeightedAverageNumberOfDilutedSharesOutstanding",
            "WeightedAverageNumberOfShareOutstandingDiluted"
        ],
        col_name="DilutedShares"
    )

    if not diluted_df.empty:
        return float(diluted_df.iloc[0]["DilutedShares"])

    # ----------------------------------
    # FALLBACK: Basic Shares
    # ----------------------------------
    basic_df = extract(
        xbrl,
        tags=[
            "WeightedAverageNumberOfSharesOutstandingBasic",
            "WeightedAverageNumberOfShareOutstandingBasic"
        ],
        col_name="BasicShares"
    )

    if not basic_df.empty:
        return float(basic_df.iloc[0]["BasicShares"])

    raise ValueError("Shares outstanding not available from 10-K")

