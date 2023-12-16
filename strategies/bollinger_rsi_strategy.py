import pandas as pd

def bollinger_rsi_strategy(data):
    # Calculate Bollinger Bands
    data['MA20'] = data['close'].rolling(window=20).mean()
    data['BB_std'] = data['close'].rolling(window=20).std()
    data['upper_band'] = data['MA20'] + (data['BB_std'] * 2)
    data['lower_band'] = data['MA20'] - (data['BB_std'] * 2)

    # Calculate the RSI (same as in the first script)
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Generate signals
    data['Buy'] = ((data['close'] < data['lower_band']) & (data['RSI'] < 30))
    data['Sell'] = ((data['close'] > data['upper_band']) & (data['RSI'] > 70))

    return data

# Example usage
# updated_data = bollinger_rsi_strategy(data)
