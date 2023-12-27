import pandas as pd
import config

def rsi_ma_strategy(data):
    # Calculate the RSI using the period from config.py
    rsi_period = config.RSI_PERIOD
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Calculate Moving Averages using periods from config.py
    short_term_period = config.SHORT_TERM_MA_PERIOD
    long_term_period = config.LONG_TERM_MA_PERIOD
    data['short_term_MA'] = data['close'].ewm(span=short_term_period, adjust=False).mean()
    data['long_term_MA'] = data['close'].ewm(span=long_term_period, adjust=False).mean()

    # Generate signals based on configured thresholds
    data['Buy'] = ((data['RSI'] > config.OVERSOLD_RSI) & (data['short_term_MA'] > data['long_term_MA']))
    data['Sell'] = ((data['RSI'] < config.OVERBOUGHT_RSI) & (data['short_term_MA'] < data['long_term_MA']))

    return data
