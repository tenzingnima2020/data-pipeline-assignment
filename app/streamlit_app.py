# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ============================================================
# 2. PAGE SETTINGS
# ============================================================
st.set_page_config(page_title="Bitcoin Statistical Analysis App", layout="wide")

# ============================================================
# 3. LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\A S U S\aidi-1204-Assignment3\data\gold\final_dataset_v2.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# ============================================================
# 4. APP TITLE
# ============================================================
st.title("Assignment 4: Bitcoin + Google Trends Statistical Analysis App")

st.markdown("""
This dashboard continues the Assignment 3 project by extending the original Gold dataset
with Google Trends search-interest data for Bitcoin.
""")

# ============================================================
# 5. SIDEBAR FILTER
# ============================================================
st.sidebar.header("Filters")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

start_date = st.sidebar.date_input(
    "Start date",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "End date",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)

if start_date > end_date:
    st.sidebar.error("Start date cannot be after end date.")
    filtered_df = df.copy()
else:
    filtered_df = df[
        (df["date"].dt.date >= start_date) &
        (df["date"].dt.date <= end_date)
    ].copy()

# ============================================================
# 6. PROJECT OVERVIEW
# ============================================================
st.header("1. Project Overview / Data Story")
st.write("""
The original project combined Bitcoin daily price data and Fear & Greed sentiment data.
This extension adds Google Trends search-interest data for Bitcoin, joined by date.
The main goal is to explore whether search-interest levels are associated with changes
in returns, volatility, positive-return frequency, and trading volume.
""")

# ============================================================
# 7. DATA PREVIEW
# ============================================================
st.header("2. Data Preview")
st.subheader("Sample of Final Dataset")
st.dataframe(filtered_df.head(10))

st.subheader("Summary Statistics")
st.dataframe(filtered_df.describe(include="all"))

st.subheader("Column Descriptions")
column_descriptions = pd.DataFrame({
    "Column": [
        "date", "btc_close", "btc_volume", "fear_greed_value", "fear_greed_label",
        "btc_daily_return", "positive_return", "is_weekend",
        "google_trends_bitcoin", "high_interest_day", "interest_group", "abs_return"
    ],
    "Meaning": [
        "Calendar date",
        "Bitcoin closing price",
        "Bitcoin trading volume",
        "Fear & Greed score",
        "Fear / Greed / Neutral label",
        "Daily Bitcoin return",
        "1 if return > 0",
        "1 if weekend",
        "Google Trends interest score",
        "1 if trend score is above median",
        "High Interest or Low Interest group",
        "Absolute daily return"
    ]
})
st.dataframe(column_descriptions)

# ============================================================
# 8. VISUAL STORYTELLING
# ============================================================
st.header("3. Visual Storytelling")

st.subheader("Chart 1: BTC Daily Return Over Time")
fig, ax = plt.subplots()
ax.plot(filtered_df["date"], filtered_df["btc_daily_return"])
ax.set_xlabel("Date")
ax.set_ylabel("BTC Daily Return")
ax.set_title("BTC Daily Return Over Time")
st.pyplot(fig)

st.subheader("Chart 2: Google Trends Interest Over Time")
fig, ax = plt.subplots()
ax.plot(filtered_df["date"], filtered_df["google_trends_bitcoin"])
ax.set_xlabel("Date")
ax.set_ylabel("Google Trends Interest")
ax.set_title("Google Trends Interest for Bitcoin Over Time")
st.pyplot(fig)

st.subheader("Chart 3: BTC Return by Interest Group")
low_group = filtered_df[filtered_df["high_interest_day"] == 0]["btc_daily_return"].dropna()
high_group = filtered_df[filtered_df["high_interest_day"] == 1]["btc_daily_return"].dropna()

fig, ax = plt.subplots()
ax.boxplot([low_group, high_group], labels=["Low Interest", "High Interest"])
ax.set_ylabel("BTC Daily Return")
ax.set_title("BTC Return by Interest Group")
st.pyplot(fig)

st.subheader("Chart 4: Google Trends vs BTC Volume")
fig, ax = plt.subplots()
ax.scatter(filtered_df["google_trends_bitcoin"], filtered_df["btc_volume"])
ax.set_xlabel("Google Trends Interest")
ax.set_ylabel("BTC Volume")
ax.set_title("Google Trends vs BTC Volume")
st.pyplot(fig)

st.subheader("Chart 5: Positive Return Counts by Interest Group")
count_table = pd.crosstab(filtered_df["high_interest_day"], filtered_df["positive_return"])
st.bar_chart(count_table)

# ============================================================
# 9. HYPOTHESIS TESTING
# ============================================================
st.header("4. Hypothesis Testing")

test_choice = st.selectbox(
    "Choose a statistical test",
    [
        "One-Sample T-Test: Mean BTC Return vs 0",
        "Two-Sample T-Test: High vs Low Interest Returns",
        "Chi-Square Test: Positive Return vs Interest Group",
        "Variance Comparison: High vs Low Interest Return Variance",
        "Correlation: Google Trends vs BTC Volume"
    ]
)

if test_choice == "One-Sample T-Test: Mean BTC Return vs 0":
    sample = filtered_df["btc_daily_return"].dropna()
    t_stat, p_val = stats.ttest_1samp(sample, 0)

    st.write("**H0:** Mean BTC daily return = 0")
    st.write("**H1:** Mean BTC daily return ≠ 0")
    st.write("**Variables:** btc_daily_return")
    st.write("**Why this fits:** one continuous variable compared to a fixed value")
    st.write(f"T-statistic: {t_stat:.4f}")
    st.write(f"P-value: {p_val:.4f}")

    if p_val < 0.05:
        st.success("The mean BTC daily return is significantly different from 0.")
    else:
        st.warning("There is not enough evidence to say the mean BTC daily return differs from 0.")

elif test_choice == "Two-Sample T-Test: High vs Low Interest Returns":
    group1 = filtered_df[filtered_df["high_interest_day"] == 1]["btc_daily_return"].dropna()
    group2 = filtered_df[filtered_df["high_interest_day"] == 0]["btc_daily_return"].dropna()

    if len(group1) < 2 or len(group2) < 2:
        st.error("Not enough data in one of the groups.")
    else:
        t_stat, p_val = stats.ttest_ind(group1, group2, equal_var=False)

        st.write("**H0:** Mean returns are the same on high-interest and low-interest days")
        st.write("**H1:** Mean returns differ between high-interest and low-interest days")
        st.write("**Variables:** btc_daily_return, high_interest_day")
        st.write("**Why this fits:** one continuous variable compared across two groups")
        st.write(f"T-statistic: {t_stat:.4f}")
        st.write(f"P-value: {p_val:.4f}")

        if p_val < 0.05:
            st.success("Returns differ significantly between high-interest and low-interest days.")
        else:
            st.warning("There is not enough evidence to say returns differ between the groups.")

elif test_choice == "Chi-Square Test: Positive Return vs Interest Group":
    contingency = pd.crosstab(filtered_df["high_interest_day"], filtered_df["positive_return"])

    if contingency.shape[0] < 2 or contingency.shape[1] < 2:
        st.error("Not enough category variation for chi-square.")
    else:
        chi2, p_val, dof, expected = stats.chi2_contingency(contingency)

        st.write("**H0:** positive_return and high_interest_day are independent")
        st.write("**H1:** positive_return and high_interest_day are associated")
        st.write("**Variables:** positive_return, high_interest_day")
        st.write("**Why this fits:** both variables are binary/categorical")
        st.dataframe(contingency)
        st.write(f"Chi-square statistic: {chi2:.4f}")
        st.write(f"P-value: {p_val:.4f}")
        st.write(f"Degrees of freedom: {dof}")

        if p_val < 0.05:
            st.success("Positive return and interest group appear associated.")
        else:
            st.warning("There is not enough evidence to conclude an association.")

elif test_choice == "Variance Comparison: High vs Low Interest Return Variance":
    group1 = filtered_df[filtered_df["high_interest_day"] == 1]["btc_daily_return"].dropna()
    group2 = filtered_df[filtered_df["high_interest_day"] == 0]["btc_daily_return"].dropna()

    if len(group1) < 2 or len(group2) < 2:
        st.error("Not enough data in one of the groups.")
    else:
        var1 = np.var(group1, ddof=1)
        var2 = np.var(group2, ddof=1)

        if var1 == 0 or var2 == 0:
            st.error("One group has zero variance.")
        else:
            if var1 > var2:
                f_stat = var1 / var2
                dfn = len(group1) - 1
                dfd = len(group2) - 1
            else:
                f_stat = var2 / var1
                dfn = len(group2) - 1
                dfd = len(group1) - 1

            p_val = 2 * min(stats.f.cdf(f_stat, dfn, dfd), 1 - stats.f.cdf(f_stat, dfn, dfd))

            st.write("**H0:** Return variances are equal across high-interest and low-interest days")
            st.write("**H1:** Return variances differ across the two groups")
            st.write("**Variables:** btc_daily_return, high_interest_day")
            st.write("**Why this fits:** compares variability of one continuous variable across two groups")
            st.write(f"F-statistic: {f_stat:.4f}")
            st.write(f"P-value: {p_val:.4f}")

            if p_val < 0.05:
                st.success("Return variability differs significantly between the groups.")
            else:
                st.warning("There is not enough evidence to say return variability differs.")

elif test_choice == "Correlation: Google Trends vs BTC Volume":
    corr_df = filtered_df[["google_trends_bitcoin", "btc_volume"]].dropna()

    if len(corr_df) < 3:
        st.error("Not enough data for correlation.")
    else:
        corr, p_val = stats.pearsonr(corr_df["google_trends_bitcoin"], corr_df["btc_volume"])

        st.write("**H0:** No linear correlation between Google Trends and BTC volume")
        st.write("**H1:** There is a linear correlation between Google Trends and BTC volume")
        st.write("**Variables:** google_trends_bitcoin, btc_volume")
        st.write("**Why this fits:** both variables are quantitative")
        st.write(f"Correlation coefficient (r): {corr:.4f}")
        st.write(f"P-value: {p_val:.4f}")

        if p_val < 0.05:
            st.success("Google Trends is significantly associated with BTC volume.")
        else:
            st.warning("There is not enough evidence to conclude a significant linear association.")

# ============================================================
# 10. REFLECTION
# ============================================================
st.header("5. Reflection / Limitations")
st.markdown("""
- Google Trends data is normalized interest, not exact search count.
- The downloaded Trends data was weekly and had to be expanded to daily rows to align with the BTC dataset.
- This assumes constant search interest within each week, which is a simplification.
- Statistical significance does not prove causation.
- Other outside factors may influence Bitcoin returns and volume.
""")