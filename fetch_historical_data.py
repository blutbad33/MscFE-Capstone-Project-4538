from binance.client import Client
import pandas as pd

# Binance API credentials
api_key = 'rbQFZbq8uQIfVDUVciOyxGjjSTRYzzMt5ca9Xsarys5i9fZMaQZvgqWy17XDpRGU'
api_secret = 'fV5xqoD2BzZ8KbO95Ug6vOC59UoHAabSquDBEv6Y4B7x4I32Q32Me7mdalrDog4V'

# Initialize the client
client = Client(api_key, api_secret)

# Define function to fetch historical data
def fetch_historical_data(symbol, start_date, end_date, interval='1h'):
    bars = client.get_historical_klines(symbol, interval, start_date, end_date)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Fetch data for BTC, ETH, and XRP from January 1, 2018, to October 30, 2023
btc_data = fetch_historical_data('BTCUSDT', '1 Jan, 2018', '30 Oct, 2023')
eth_data = fetch_historical_data('ETHUSDT', '1 Jan, 2018', '30 Oct, 2023')
xrp_data = fetch_historical_data('XRPUSDT', '1 Jan, 2018', '30 Oct, 2023')

# Save data to the main directory with specified filenames
btc_data.to_csv('BTCUSDT_data.csv', index=False)
eth_data.to_csv('ETHUSDT_data.csv', index=False)
xrp_data.to_csv('XRPUSDT_data.csv', index=False)
