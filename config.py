# config.py

# Configuration for Binance API Calls
API_KEY = 'rbQFZbq8uQIfVDUVciOyxGjjSTRYzzMt5ca9Xsarys5i9fZMaQZvgqWy17XDpRGU'
API_SECRET = 'fV5xqoD2BzZ8KbO95Ug6vOC59UoHAabSquDBEv6Y4B7x4I32Q32Me7mdalrDog4V'

# Trading configuration with 1hour trading interval configuration
TRADING_PAIRS = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT']  # Cryptocurrency pairs to trade
TRADE_INTERVAL = '1h'  # Trading interval

# Technical analysis settings for RSI and Moving Average Strategy
RSI_PERIOD = 14  # Period for Relative Strength Index
OVERBOUGHT_RSI = 70
OVERSOLD_RSI = 30
SHORT_TERM_MA_PERIOD = 9  # Period for short-term EMA
LONG_TERM_MA_PERIOD = 21  # Period for long-term EMA

# Technical analysis settings for Bollinger Bands and RSI Strategy
BOLLINGER_BANDS_PERIOD = 20  # Period for Bollinger Bands
BOLLINGER_BANDS_STD_DEV = 2  # Standard deviation for Bollinger Bands

# Risk management
INITIAL_CAPITAL = 10000  # Starting capital in USD
RISK_PER_TRADE = 0.5  # Risk 0.5% of account balance per trade
STOP_LOSS_PERCENTAGE = 0.5  # Stop loss percentage set to 0.5% per trade
TAKE_PROFIT_PERCENTAGE = 1  # Take profit percentage set to 1% per trade

# Other configurations
LOG_LEVEL = 'INFO'  # Logging level (DEBUG, INFO, WARNING, ERROR)
