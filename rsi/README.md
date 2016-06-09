-- Notes:
RSI ML Strat:

- Decision tree
- Logistic regression

RSI daily
-- 14 day
-- 9 day
-- Diff defs of overbought & over sold

Strat
-> Buy oversold on daily
-> Sell on overbought

Params
-- Stock $5 >=
-- Market Cap >= 400mm
-- Daily Vol >= 600k shares

•Compare ML to backtest
•Figure out data acquistion
•Lookback period?

-- Installs:
`conda install -c anaconda quandl=2.8.9`
`conda create --name rsi --file requirements.txt`

-- Environments:
`source activate rsi`