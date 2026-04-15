# ============================================================
# STREAMLIT APP — ASSIGNMENT 4
# BTC + FEAR/GREED + GOOGLE TRENDS
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, ttest_1samp, ttest_ind, levene, spearmanr
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Bitcoin Statistical Analysis App",
    page_icon="📈",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\A S U S\aidi-1204-Assignment3\data\gold\final_dataset_v2.csv")

    # Clean date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Sort by date
    df = df.sort_values("date").reset_index(drop=True)

    # Ensure needed numeric columns
    numeric_cols = [
        "btc_close",
        "btc_volume",
        "fear_greed_value",
        "btc_daily_return",
        "positive_return",
        "google_trends_bitcoin",
        "high_interest_day",
        "abs_return"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Ensure positive_return is numeric
    if "positive_return" in df.columns:
        if df["positive_return"].dtype == object:
            df["positive_return"] = df["positive_return"].map(
                {"Yes": 1, "No": 0, "yes": 1, "no": 0, "True": 1, "False": 0, "1": 1, "0": 0}
            ).fillna(df["positive_return"])
        df["positive_return"] = pd.to_numeric(df["positive_return"], errors="coerce")

    # Temporary readable label for charts only
    if "high_interest_day" in df.columns:
        df["high_interest_label"] = np.where(
            df["high_interest_day"] == 1,
            "High Interest",
            "Low Interest"
        )

    return df


df = load_data()

# ============================================================
# TITLE / INTRO
# ============================================================
st.title("📈 Bitcoin, Sentiment, and Search Interest Dashboard")
st.markdown("""
This app extends the original Bitcoin Gold dataset by adding **Google Trends** data as a new external source.
The project explores whether **search interest**, **sentiment**, and **market behavior** are associated with
changes in Bitcoin returns and trading volume.
""")

# ============================================================
# SIDEBAR FILTERS
# ============================================================
st.sidebar.header("Filters")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

fear_labels = sorted(df["fear_greed_label"].dropna().unique().tolist()) if "fear_greed_label" in df.columns else []
selected_fear = st.sidebar.multiselect(
    "Fear/Greed Label",
    options=fear_labels,
    default=fear_labels
)

interest_options = sorted(df["interest_group"].dropna().unique().tolist()) if "interest_group" in df.columns else []
selected_interest = st.sidebar.multiselect(
    "Google Trends Interest Group",
    options=interest_options,
    default=interest_options
)

show_positive_only = st.sidebar.checkbox("Show Positive Return Days Only", value=False)

# Apply filters
filtered_df = df.copy()

filtered_df = filtered_df[
    (filtered_df["date"] >= pd.to_datetime(start_date)) &
    (filtered_df["date"] <= pd.to_datetime(end_date))
]

if "fear_greed_label" in filtered_df.columns and selected_fear:
    filtered_df = filtered_df[filtered_df["fear_greed_label"].isin(selected_fear)]

if "interest_group" in filtered_df.columns and selected_interest:
    filtered_df = filtered_df[filtered_df["interest_group"].isin(selected_interest)]

if show_positive_only and "positive_return" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["positive_return"] == 1]

# ============================================================
# KPI CARDS
# ============================================================
st.markdown("## Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Rows in View", len(filtered_df))

with col2:
    avg_return = filtered_df["btc_daily_return"].mean() if "btc_daily_return" in filtered_df.columns else np.nan
    st.metric("Avg Daily Return", f"{avg_return:.4f}" if pd.notna(avg_return) else "N/A")

with col3:
    avg_volume = filtered_df["btc_volume"].mean() if "btc_volume" in filtered_df.columns else np.nan
    st.metric("Avg Volume", f"{avg_volume:,.0f}" if pd.notna(avg_volume) else "N/A")

with col4:
    avg_trends = filtered_df["google_trends_bitcoin"].mean() if "google_trends_bitcoin" in filtered_df.columns else np.nan
    st.metric("Avg Google Trends", f"{avg_trends:.2f}" if pd.notna(avg_trends) else "N/A")

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Project Overview",
    "Data Preview",
    "Visual Storytelling",
    "Hypothesis Testing",
    "Reflection / Limitations"
])

# ============================================================
# TAB 1 — PROJECT OVERVIEW
# ============================================================
with tab1:
    st.subheader("Project Story")

    st.markdown("""
### Original Assignment 3 Dataset
The original Gold dataset combined:
- **Bitcoin market data**
- **Fear and Greed sentiment data**

### New External Source Added
For Assignment 4, the project adds:
- **Google Trends data for Bitcoin search interest**

### Join Strategy
The datasets were joined using:
- **`date`** as the common key

### Why Google Trends Matters
Google Trends adds behavioral context by capturing public attention toward Bitcoin.
This does not prove causation, but it may be associated with:
- higher trading activity,
- changes in returns,
- and shifts in market behavior.

### Main Analytical Questions
1. Is the mean daily Bitcoin return different from 0?
2. Do returns differ on high-interest vs low-interest days?
3. Is positive return independent of search-interest group?
4. Is return variability different across interest groups?
5. Is Google search interest associated with Bitcoin trading volume?
""")

# ============================================================
# TAB 2 — DATA PREVIEW
# ============================================================
with tab2:
    st.subheader("Dataset Preview")

    st.write("### Sample Data")
    st.dataframe(filtered_df.head(20), use_container_width=True)

    st.write("### Summary Statistics")
    st.dataframe(filtered_df.describe(include="all").T, use_container_width=True)

    st.write("### Column Descriptions")
    column_info = pd.DataFrame({
        "Column": [
            "date",
            "btc_close",
            "btc_volume",
            "fear_greed_value",
            "fear_greed_label",
            "btc_daily_return",
            "positive_return",
            "is_weekend",
            "google_trends_bitcoin",
            "high_interest_day",
            "interest_group",
            "abs_return"
        ],
        "Description": [
            "Date of observation",
            "Bitcoin closing price",
            "Bitcoin trading volume",
            "Fear and Greed index value",
            "Fear and Greed category label",
            "Daily Bitcoin return",
            "1 if daily return > 0, otherwise 0",
            "Weekend indicator",
            "Google Trends score for Bitcoin",
            "Binary indicator for high-interest day",
            "Google Trends grouping category",
            "Absolute value of daily return"
        ]
    })
    st.dataframe(column_info, use_container_width=True)

# ============================================================
# TAB 3 — VISUAL STORYTELLING
# ============================================================
with tab3:
    st.subheader("Visual Storytelling")

    # Chart 1
    st.markdown("### 1. Daily Bitcoin Returns Over Time")
    fig1 = px.line(
        filtered_df,
        x="date",
        y="btc_daily_return",
        title="Daily Bitcoin Returns Over Time"
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("This time-series chart helps show changes in daily returns over time and highlights volatility in the market.")

    # Chart 2
    st.markdown("### 2. Bitcoin Trading Volume Over Time")
    fig2 = px.line(
        filtered_df,
        x="date",
        y="btc_volume",
        title="Bitcoin Trading Volume Over Time"
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("This chart shows how trading activity changes over time and supports later comparisons with Google search interest.")

    # Chart 3
    st.markdown("### 3. Returns by Google Search Interest Group")
    if "high_interest_label" in filtered_df.columns:
        fig3 = px.box(
            filtered_df,
            x="high_interest_label",
            y="btc_daily_return",
            color="high_interest_label",
            title="Bitcoin Returns on High vs Low Interest Days"
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("This grouped boxplot compares return distributions across high-interest and low-interest days.")
    else:
        st.warning("`high_interest_day` column not found.")

    # Chart 4
    st.markdown("### 4. Positive vs Non-Positive Return Days by Search Interest")
    if "high_interest_label" in filtered_df.columns and "positive_return" in filtered_df.columns:
        count_df = filtered_df.copy()
        count_df["positive_return_label"] = np.where(
            count_df["positive_return"] == 1,
            "Positive",
            "Non-Positive"
        )
        count_df = count_df.groupby(["high_interest_label", "positive_return_label"]).size().reset_index(name="count")

        fig4 = px.bar(
            count_df,
            x="high_interest_label",
            y="count",
            color="positive_return_label",
            barmode="group",
            title="Return Direction by Search Interest Group"
        )
        st.plotly_chart(fig4, use_container_width=True)
        st.caption("This grouped bar chart shows categorical count differences across high-interest and low-interest days.")
    else:
        st.warning("Required columns for categorical chart are missing.")

    # Chart 5
    st.markdown("### 5. Google Trends vs Bitcoin Volume")
    if "google_trends_bitcoin" in filtered_df.columns and "btc_volume" in filtered_df.columns:
        fig5 = px.scatter(
            filtered_df,
            x="google_trends_bitcoin",
            y="btc_volume",
            color="fear_greed_label" if "fear_greed_label" in filtered_df.columns else None,
            hover_data=["date"],
            title="Google Search Interest vs Bitcoin Trading Volume"
        )
        st.plotly_chart(fig5, use_container_width=True)
        st.caption("This scatterplot shows whether higher search interest aligns with higher trading volume.")
    else:
        st.warning("Google Trends or BTC volume column missing.")

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def safe_dropna(series):
    return pd.to_numeric(series, errors="coerce").dropna()

def interpret_pvalue(p):
    if p < 0.05:
        return "The result is statistically significant at the 5% level."
    return "The result is not statistically significant at the 5% level."

# ============================================================
# TAB 4 — HYPOTHESIS TESTING
# ============================================================
with tab4:
    st.subheader("Hypothesis Testing")

    test_option = st.selectbox(
        "Choose a statistical analysis",
        [
            "One-Sample T-Test: Mean BTC Return vs 0",
            "Two-Sample T-Test: Returns on High vs Low Interest Days",
            "Chi-Square Test: Positive Return vs Search Interest",
            "Variance Comparison: Return Variability by Interest Group",
            "Correlation: Google Trends vs BTC Volume"
        ]
    )

    if test_option == "One-Sample T-Test: Mean BTC Return vs 0":
        st.markdown("### One-Sample T-Test")
        st.write("**Null Hypothesis (H₀):** The mean daily Bitcoin return is equal to 0.")
        st.write("**Alternative Hypothesis (H₁):** The mean daily Bitcoin return is not equal to 0.")

        sample = safe_dropna(filtered_df["btc_daily_return"])
        if len(sample) > 1:
            t_stat, p_val = ttest_1samp(sample, popmean=0)

            st.write(f"**Sample Size:** {len(sample)}")
            st.write(f"**Mean Return:** {sample.mean():.6f}")
            st.write(f"**T-Statistic:** {t_stat:.4f}")
            st.write(f"**P-Value:** {p_val:.6f}")
            st.write(interpret_pvalue(p_val))
        else:
            st.warning("Not enough data to run the one-sample t-test.")

    elif test_option == "Two-Sample T-Test: Returns on High vs Low Interest Days":
        st.markdown("### Two-Sample T-Test")
        st.write("**Null Hypothesis (H₀):** Mean daily BTC return is the same on high-interest and low-interest days.")
        st.write("**Alternative Hypothesis (H₁):** Mean daily BTC return differs between high-interest and low-interest days.")

        if "high_interest_day" in filtered_df.columns:
            g1 = safe_dropna(filtered_df.loc[filtered_df["high_interest_day"] == 1, "btc_daily_return"])
            g2 = safe_dropna(filtered_df.loc[filtered_df["high_interest_day"] == 0, "btc_daily_return"])

            if len(g1) > 1 and len(g2) > 1:
                t_stat, p_val = ttest_ind(g1, g2, equal_var=False)

                st.write(f"**High Interest Group Size:** {len(g1)}")
                st.write(f"**Low Interest Group Size:** {len(g2)}")
                st.write(f"**High Interest Mean:** {g1.mean():.6f}")
                st.write(f"**Low Interest Mean:** {g2.mean():.6f}")
                st.write(f"**T-Statistic:** {t_stat:.4f}")
                st.write(f"**P-Value:** {p_val:.6f}")
                st.write(interpret_pvalue(p_val))
            else:
                st.warning("Not enough data in one or both groups.")
        else:
            st.warning("`high_interest_day` column not found.")

    elif test_option == "Chi-Square Test: Positive Return vs Search Interest":
        st.markdown("### Chi-Square Test of Independence")
        st.write("**Null Hypothesis (H₀):** Positive return is independent of search-interest group.")
        st.write("**Alternative Hypothesis (H₁):** Positive return is associated with search-interest group.")

        if "high_interest_day" in filtered_df.columns and "positive_return" in filtered_df.columns:
            contingency = pd.crosstab(filtered_df["high_interest_day"], filtered_df["positive_return"])

            if contingency.shape[0] >= 2 and contingency.shape[1] >= 2:
                chi2, p_val, dof, expected = chi2_contingency(contingency)

                contingency.index = ["Low Interest" if x == 0 else "High Interest" for x in contingency.index]
                contingency.columns = ["Non-Positive" if x == 0 else "Positive" for x in contingency.columns]

                st.write("**Contingency Table**")
                st.dataframe(contingency, use_container_width=True)

                st.write(f"**Chi-Square Statistic:** {chi2:.4f}")
                st.write(f"**Degrees of Freedom:** {dof}")
                st.write(f"**P-Value:** {p_val:.6f}")

                expected_df = pd.DataFrame(expected, index=contingency.index, columns=contingency.columns)
                st.write("**Expected Counts**")
                st.dataframe(expected_df, use_container_width=True)

                st.write(interpret_pvalue(p_val))
            else:
                st.warning("Contingency table does not have enough categories.")
        else:
            st.warning("Required categorical columns are missing.")

    elif test_option == "Variance Comparison: Return Variability by Interest Group":
        st.markdown("### Variance Comparison")
        st.write("**Null Hypothesis (H₀):** Return variability is the same for high-interest and low-interest days.")
        st.write("**Alternative Hypothesis (H₁):** Return variability differs between the two groups.")

        if "high_interest_day" in filtered_df.columns:
            g1 = safe_dropna(filtered_df.loc[filtered_df["high_interest_day"] == 1, "btc_daily_return"])
            g2 = safe_dropna(filtered_df.loc[filtered_df["high_interest_day"] == 0, "btc_daily_return"])

            if len(g1) > 1 and len(g2) > 1:
                stat, p_val = levene(g1, g2, center="median")

                st.write(f"**High Interest Variance:** {np.var(g1, ddof=1):.6f}")
                st.write(f"**Low Interest Variance:** {np.var(g2, ddof=1):.6f}")
                st.write(f"**Levene Statistic:** {stat:.4f}")
                st.write(f"**P-Value:** {p_val:.6f}")
                st.write(interpret_pvalue(p_val))
            else:
                st.warning("Not enough data in one or both groups.")
        else:
            st.warning("`high_interest_day` column not found.")

    elif test_option == "Correlation: Google Trends vs BTC Volume":
        st.markdown("### Correlation Analysis")
        st.write("**Null Hypothesis (H₀):** There is no monotonic association between Google Trends and BTC trading volume.")
        st.write("**Alternative Hypothesis (H₁):** There is a monotonic association between Google Trends and BTC trading volume.")

        if "google_trends_bitcoin" in filtered_df.columns and "btc_volume" in filtered_df.columns:
            corr_df = filtered_df[["google_trends_bitcoin", "btc_volume"]].dropna()

            if len(corr_df) > 2:
                rho, p_val = spearmanr(corr_df["google_trends_bitcoin"], corr_df["btc_volume"])

                st.write(f"**Sample Size:** {len(corr_df)}")
                st.write(f"**Spearman Correlation (rho):** {rho:.4f}")
                st.write(f"**P-Value:** {p_val:.6f}")
                st.write(interpret_pvalue(p_val))
            else:
                st.warning("Not enough paired observations for correlation analysis.")
        else:
            st.warning("Google Trends or BTC volume column missing.")

# ============================================================
# TAB 5 — REFLECTION / LIMITATIONS
# ============================================================
with tab5:
    st.subheader("Reflection / Limitations")

    st.markdown("""
### Important Assumptions
- Observations are treated as daily records and assumed to be reasonably independent.
- T-tests assume a meaningful comparison of group means.
- Chi-square assumes categorical counts with reasonable expected frequencies.
- Correlation assumes paired observations and interprets association, not causation.

### Limitations of the Data
- Crypto returns are volatile and may include outliers.
- Google Trends is a normalized search-interest measure, not a direct measure of investor intent.
- Sentiment categories and search-interest groups simplify real market behavior.
- Daily joins by `date` can hide within-day timing differences between attention, sentiment, and trading activity.

### Join Issues
- Different sources may use different calendars or update times.
- Missing days or mismatched timestamps can affect the final merged dataset.

### Why Significance Is Not the Same as Importance
A statistically significant result does not automatically mean the effect is large or practically important.
It also does not imply causation. External factors such as macroeconomic announcements, regulation, or news events
may influence both search interest and market behavior at the same time.

### If This Became a Larger Product
Possible future improvements:
- add macroeconomic event days,
- add holiday indicators,
- include volatility-specific metrics,
- compare multiple cryptocurrencies,
- and improve time alignment across sources.
""")