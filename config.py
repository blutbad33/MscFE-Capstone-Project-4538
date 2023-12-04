# config.py

# Binance API configuration
API_KEY = 'your_binance_api_key'
API_SECRET = 'your_binance_api_secret'

# Trading configuration
TRADING_PAIRS = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT']  # Cryptocurrency pairs to trade
TRADE_INTERVAL = '1h'  # Trading interval

# Technical analysis settings
RSI_PERIOD = 14  # Period for Relative Strength Index
MA_PERIOD = 50  # Period for Moving Average
BB_PERIOD = 20  # Period for Bollinger Bands
BB_STD_DEV = 2  # Standard deviation for Bollinger Bands

# Risk management
MAX_TRADE_QUANTITY = 10  # Maximum quantity to trade
STOP_LOSS_PERCENTAGE = 5  # Stop loss percentage
TAKE_PROFIT_PERCENTAGE = 10  # Take profit percentage

# Other configurations
LOG_LEVEL = 'INFO'  # Logging level (DEBUG, INFO, WARNING, ERROR)
