
import requests
import pandas as pd

# -------------------------------------------------
# GLOBAL SETTINGS
# -------------------------------------------------
SEC_HEADERS = {
    "User-Agent": "YourName your.email@example.com"
}

SEC_TICKER_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_XBRL_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"


# -------------------------------------------------
# TICKER → CIK
# -------------------------------------------------
def get_cik_from_ticker(ticker: str) -> str:
    """
    Convert ticker to zero-padded CIK using SEC mapping
    """
    r = requests.get(SEC_TICKER_URL, headers=SEC_HEADERS)
    r.raise_for_status()
    data = r.json()

    ticker = ticker.upper()

    for _, item in data.items():
        if item["ticker"] == ticker:
            return str(item["cik_str"]).zfill(10)

    raise ValueError(f"CIK not found for ticker: {ticker}")


# -------------------------------------------------
# DOWNLOAD COMPANY XBRL JSON
# -------------------------------------------------
def get_company_xbrl(cik: str) -> dict:
    """
    Download company XBRL facts JSON from SEC
    """
    url = SEC_XBRL_URL.format(cik=cik)
    r = requests.get(url, headers=SEC_HEADERS)
    r.raise_for_status()
    return r.json()


# -------------------------------------------------
# EXTRACT TIME SERIES FROM XBRL
# -------------------------------------------------
def extract_series(xbrl: dict, tags: list[str], col_name: str) -> pd.DataFrame:
    """
    Extract annual USD values for given XBRL tags
    """
    records = []

    facts = xbrl.get("facts", {}).get("us-gaap", {})

    for tag in tags:
        tag_data = facts.get(tag, {})
        units = tag_data.get("units", {}).get("USD", [])

        for item in units:
            if item.get("form") == "10-K":
                year = int(item["fy"])
                value = item["val"]

                records.append({
                    "Year": year,
                    col_name: value
                })

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)
    return (
        df.sort_values("Year", ascending=False)
          .drop_duplicates("Year")
          .reset_index(drop=True)
    )
