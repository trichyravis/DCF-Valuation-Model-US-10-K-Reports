
import streamlit as st
import pandas as pd

# -------------------------------
# INTERNAL MODULE IMPORTS
# -------------------------------
from modules.data_fetcher import (
    get_cik_from_ticker,
    get_company_xbrl,
    extract_series
)

from modules.company_classifier import classify_company

# FCFF / Operating-company modules
from modules.base_year import get_base_year_operating_data
from modules.fcff_projection import project_fcff
from modules.dcf import dcf_valuation
from modules.wacc import calculate_wacc
from modules.net_debt import get_net_debt
from modules.equity import get_share_count


# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="US 10-K Valuation Platform",
    layout="wide"
)

st.title("📊 US 10-K Based Valuation Platform")

st.info(
    "Professional valuation workflow:\n"
    "• Download audited SEC 10-K data\n"
    "• Classify company economics\n"
    "• Apply the correct valuation model\n\n"
    "⚠️ FCFF is used only for non-financial operating companies."
)

# -------------------------------
# USER INPUT
# -------------------------------
ticker = st.text_input(
    "Enter US Ticker (Audited 10-K Search)",
    value="AAPL"
).upper()

run_button = st.button("🚀 Run Valuation")

# -------------------------------
# MAIN EXECUTION
# -------------------------------
if run_button:

    try:
        # ---------------------------
        # LOAD SEC DATA
        # ---------------------------
        cik = get_cik_from_ticker(ticker)
        xbrl = get_company_xbrl(cik)

        st.subheader("📁 SEC Filing Metadata")
        st.json({
            "Ticker": ticker,
            "CIK": cik,
            "Source": "SEC EDGAR (XBRL)",
            "Filing Type": "10-K"
        })

        # ---------------------------
        # CLASSIFY COMPANY
        # ---------------------------
        company_type = classify_company(xbrl, extract_series)

        st.subheader("🏷️ Company Classification")
        st.info(f"Detected Company Type: **{company_type}**")

        # ==========================================================
        # FINANCIAL INSTITUTIONS — STOP HERE (FOR NOW)
        # ==========================================================
        if company_type == "Financial":

            st.error(
                "🚫 This company is a **financial institution** "
                "(bank / NBFC / insurer).\n\n"
                "• EBIT, FCFF, and Enterprise Value are **not defined**\n"
                "• Debt is operating capital, not financing\n\n"
                "👉 Use **FCFE / Dividend Discount** models instead."
            )

            st.info(
                "Next step:\n"
                "We will add a **bank-specific FCFE valuation module** "
                "to handle companies like JPM correctly."
            )

            st.stop()

        # ==========================================================
        # NON-FINANCIAL OPERATING COMPANIES — FCFF MODEL
        # ==========================================================

        # ---------------------------
        # BASE-YEAR ECONOMICS
        # ---------------------------
        base = get_base_year_operating_data(
            xbrl,
            extract_series
        )

        st.subheader("📘 Base-Year Operating Economics (Latest 10-K)")

        c1, c2, c3 = st.columns(3)
        c1.metric("Revenue ($bn)", f"{base['revenue']/1e9:,.1f}")
        c2.metric("Operating Margin", f"{base['operating_margin']:.1%}")
        c3.metric("Effective Tax Rate", f"{base['tax_rate']:.1%}")

        # ---------------------------
        # USER ASSUMPTIONS
        # ---------------------------
        st.subheader("🧠 Growth & Reinvestment Assumptions")

        growth_rates = st.multiselect(
            "Revenue Growth Assumptions (Next 5 Years)",
            [0.04, 0.06, 0.08, 0.10, 0.12, 0.15],
            default=[0.10, 0.10, 0.10, 0.08, 0.08]
        )

        if len(growth_rates) != 5:
            st.warning("Please select exactly 5 growth rates.")
            st.stop()

        sales_to_capital = st.slider(
            "Sales-to-Capital Ratio (Capital Efficiency)",
            min_value=1.0,
            max_value=6.0,
            value=2.5,
            step=0.1
        )

        terminal_growth = st.slider(
            "Terminal Growth Rate",
            min_value=0.02,
            max_value=0.04,
            value=0.03,
            step=0.005
        )

        # ---------------------------
        # FCFF PROJECTION
        # ---------------------------
        projections = project_fcff(
            base_revenue=base["revenue"],
            operating_margin=base["operating_margin"],
            tax_rate=base["tax_rate"],
            growth_rates=growth_rates,
            sales_to_capital=sales_to_capital
        )

        df_fcff = pd.DataFrame(projections)
        df_fcff["Revenue ($bn)"] = df_fcff["Revenue"] / 1e9
        df_fcff["Reinvestment ($bn)"] = df_fcff["Reinvestment"] / 1e9
        df_fcff["FCFF ($bn)"] = df_fcff["FCFF"] / 1e9

        st.subheader("📗 FCFF Forecast (Base Year + Explicit Period)")
        st.dataframe(
            df_fcff[
                ["Year", "Revenue ($bn)", "Reinvestment ($bn)", "FCFF ($bn)"]
            ],
            use_container_width=True
        )

        # ---------------------------
        # COST OF CAPITAL
        # ---------------------------
        wacc_data = calculate_wacc(ticker)
        wacc = wacc_data["WACC"]

        st.subheader("📐 Cost of Capital")
        st.metric("WACC (CAPM-Based)", f"{wacc:.2%}")

        # ---------------------------
        # ROIC VS WACC DIAGNOSTIC
        # ---------------------------
        roic = (
            base["operating_margin"]
            * (1 - base["tax_rate"])
            * sales_to_capital
        )

        st.subheader("🧮 Growth Economics Diagnostic")

        c1, c2 = st.columns(2)
        c1.metric("Implied ROIC", f"{roic:.1%}")
        c2.metric("WACC", f"{wacc:.1%}")

        if roic < wacc:
            st.error(
                "Growth is **value destructive** (ROIC < WACC).\n"
                "Negative FCFF during high-growth years is expected."
            )
        else:
            st.success(
                "Growth is **value creating** (ROIC > WACC)."
            )

        # ---------------------------
        # DCF VALUATION
        # ---------------------------
        valuation = dcf_valuation(
            fcff_projection=projections,
            wacc=wacc,
            terminal_growth=terminal_growth
        )

        enterprise_value = valuation["enterprise_value"]

        # ---------------------------
        # EQUITY VALUE
        # ---------------------------
        net_debt = get_net_debt(xbrl, extract_series)
        shares = get_share_count(xbrl)

        equity_value = enterprise_value - net_debt
        fair_value = equity_value / shares if shares > 0 else None

        st.subheader("📈 Valuation Summary")

        c1, c2, c3 = st.columns(3)
        c1.metric("Enterprise Value ($bn)", f"{enterprise_value/1e9:,.0f}")
        c2.metric("Equity Value ($bn)", f"{equity_value/1e9:,.0f}")
        c3.metric(
            "Fair Value per Share",
            f"${fair_value:,.2f}" if fair_value else "N/A"
        )

        # ---------------------------
        # NOTES
        # ---------------------------
        st.info(
            "Interpretation Notes:\n"
            "• FCFF = NOPAT − Reinvestment\n"
            "• High growth requires capital; FCFF may be negative\n"
            "• Value is created only when ROIC exceeds WACC\n"
            "• Terminal value drives most intrinsic value"
        )

    except Exception as e:
        st.exception(e)
