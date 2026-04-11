# Assignment 4 Analysis Plan

## Original Project
In Assignment 3, I built a Gold dataset by combining Bitcoin daily market data from Binance with Fear & Greed sentiment data.

## New External Source
For Assignment 4, I added Google Trends search interest data for the term "Bitcoin".

## Why This Source Matters
Google Trends provides a measure of public attention. This helps explore whether higher interest in Bitcoin is associated with changes in returns, positive-return frequency, and trading volume.

## Join Key
The Google Trends dataset was joined to the existing Gold dataset using the `date` column.

## New Variables Created
- `google_trends_bitcoin`: daily search-interest score
- `high_interest_day`: 1 if search interest is above median, else 0
- `interest_group`: High Interest or Low Interest
- `abs_return`: absolute BTC daily return

## Main Story
The dashboard explores whether public search interest in Bitcoin is associated with differences in returns, volatility, and trading volume.

## Planned Analyses
1. One-sample t-test: Is mean BTC daily return different from 0?
2. Two-sample t-test: Do BTC returns differ between high-interest and low-interest days?
3. Chi-square test: Is positive_return associated with high_interest_day?
4. Variance comparison: Does return variability differ between high-interest and low-interest days?
5. Correlation analysis: Is Google Trends associated with BTC volume?