import pandas as pd
import config
from datetime import timedelta

def rsi_ma_strategy(data):
    # Calculate the RSI using period from config.py
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

    # Generate signals with additional conditions
    for i in range(len(data)):
        data.loc[i, 'Buy'] = False
        data.loc[i, 'Sell'] = False
        if i > 0 and not pd.isnull(data.loc[i, 'RSI']):
            # Buy condition
            if (data.loc[i, 'RSI'] > 30) & (data.loc[i, 'short_term_MA'] > data.loc[i, 'long_term_MA']):
                data.loc[i, 'Buy'] = True
                # Check for sell condition within 1 day
                sell_date = data.loc[i, 'timestamp'] + timedelta(days=1)
                sell_index = data[(data['timestamp'] >= sell_date)].index.min()
                if sell_index and sell_index < len(data):
                    data.loc[sell_index, 'Sell'] = True
            # Sell condition
            elif (data.loc[i, 'RSI'] < 70) & (data.loc[i, 'short_term_MA'] < data.loc[i, 'long_term_MA']):
                data.loc[i, 'Sell'] = True

    # Trade size calculation (an example approach)
    data['Trade Size'] = data.apply(lambda row: calculate_trade_size(row['timestamp'], row['close']), axis=1)

    return data

def calculate_trade_size(timestamp, price):
    # Example trade size calculation based on volatility or other factors
    # Adjust this function according to your strategy
    if timestamp.hour < 12:
        return config.INITIAL_CAPITAL * 0.01  # 1% of capital for morning trades
    else:
        return config.INITIAL_CAPITAL * 0.02  # 2% of capital for afternoon trades

# Example usage

