import pandas as pd
import config

def bollinger_rsi_strategy(data):
    # Calculate Bollinger Bands using parameters from config.py
    window = config.BOLLINGER_BANDS_PERIOD
    std_dev = config.BOLLINGER_BANDS_STD_DEV
    data['MA20'] = data['close'].rolling(window=window).mean()
    data['BB_std'] = data['close'].rolling(window=window).std()
    data['upper_band'] = data['MA20'] + (data['BB_std'] * std_dev)
    data['lower_band'] = data['MA20'] - (data['BB_std'] * std_dev)

    # Calculate the RSI using period from config.py
    rsi_period = config.RSI_PERIOD
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Generate signals
    data['Buy'] = (data['close'] < data['lower_band']) & (data['RSI'] < config.OVERSOLD_RSI)
    data['Sell'] = (data['close'] > data['upper_band']) & (data['RSI'] > config.OVERBOUGHT_RSI)

    return data
