import pandas as pd

def rsi_ma_strategy(data):
    # Calculate the RSI
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Calculate Moving Averages
    data['short_term_MA'] = data['close'].ewm(span=9, adjust=False).mean()
    data['long_term_MA'] = data['close'].ewm(span=21, adjust=False).mean()

    # Generate signals
    data['Buy'] = ((data['RSI'] > 30) & (data['short_term_MA'] > data['long_term_MA']))
    data['Sell'] = ((data['RSI'] < 70) & (data['short_term_MA'] < data['long_term_MA']))

    return data

# Example usage (assuming 'data' is a DataFrame with close prices)
# updated_data = rsi_ma_strategy(data)
