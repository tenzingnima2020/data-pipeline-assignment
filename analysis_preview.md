# Statistical Analysis Preview

## 1. Statistical Question
Is the mean daily BTC return different from 0?
Do BTC returns differ on Fear days vs Greed days?
Is the proportion of positive-return days higher on Greed days?

## 2. Outcome Variable
`btc_daily_return` — the percentage change in BTC closing price day over day.

## 3. Grouping Variable
`fear_greed_label` — categorizes each day as Fear, Greed, Neutral, etc.

## 4. Binary Variable
`positive_return` — 1 if BTC return was positive that day, 0 if negative.
Created to support proportion-based z-tests in Part 2.

## 5. Hypotheses
- H0: Mean daily BTC return = 0
- H1: Mean daily BTC return ≠ 0

- H0: Mean return on Fear days = Mean return on Greed days
- H1: Mean return on Fear days ≠ Mean return on Greed days

## 6. Best Test
- One-sample t-test to check if mean return differs from 0
- Two-sample t-test to compare Fear vs Greed days
- Proportion z-test to compare positive return rates across sentiment groups