# MscFE-Capstone-Project-4538


```markdown
# Cryptocurrency Short-Term Trading Model

This repository hosts a Python-based trading model designed for short-term trading in cryptocurrencies Bitcoin (BTC), Ethereum (ETH), and Ripple (XRP). The Cryptocurrency Short-Term Trading Model operates by simulating trades on historical price data for Bitcoin (BTC), Ethereum (ETH), and Ripple (XRP) from January 1, 2018, to October 30, 2023 Integrated with the Binance API for historical data collection. It employs two distinct strategies—RSI with Moving Averages and Bollinger Bands with RSI—to identify optimal buy and sell points. The model, starting with an initial capital of $10,000, assesses each strategy's performance in terms of profitability and risk, using detailed trade data to calculate metrics like Sharpe ratio and drawdown percentage. 

For more information about the project, visit the [project page](https://github.com/blutbad33/MscFE-Capstone-Project-4538/new/main?readme=1).

## Table of Contents

- Requirements
- Recommended Libraries
- Installation
- Configuration
- Troubleshooting
- FAQ
- Maintainers

## Project Structure

- `main.py`: The main script to run the trading model using historical data.
- `fetch_historical_data.py`: Script to fetch historical data for BTC, ETH, and XRP from the Binance API.
- `analysis/analysis.py`: A detailed analysis script for evaluating trading performance and statistics.
- `strategies/`: Directory containing trading strategy scripts.
  - `rsi_ma_strategy.py`: Strategy based on RSI and Moving Averages.
  - `bollinger_rsi_strategy.py`: Strategy using Bollinger Bands and RSI.
- `data/`: Directory for storing historical data fetched by `fetch_historical_data.py`.
- `BinanceAPI.env`: Environment file to store Binance API keys (not included in the repository for security).
- `config.py`: Configuration file for trading parameters and API keys.
- `requirements.txt`: Required libraries for the project.
- `README.md`: This file, containing project information and setup instructions.
- `LICENSE`: The MIT License for the project.
- `CONTRIBUTING.md`: Guidelines for contributing to the project.

## Requirements

This project requires the following modules:

- Python 3.6 or higher
- Binance API
- [scikit-learn](https://scikit-learn.org/stable/)
- Other Python libraries: pandas, NumPy, Matplotlib

## Recommended Libraries

- [TA-Lib](https://www.ta-lib.org/) for technical analysis indicators.
- [TensorFlow](https://www.tensorflow.org/) or [PyTorch](https://pytorch.org/) for advanced machine learning models.

## Installation

Clone the repository and install the required Python packages:

```bash
git clone https://github.com/blutbad33/MscFE-Capstone-Project-4538.git
cd cryptocurrency-trading-model
pip install -r requirements.txt
python fetch_historical_data.py
python main.py
python analysis/analysis.py

```

## Configuration

1. Set up our Binance API keys and store them in a `.env` file:

   ```
   BINANCE_API_KEY='your-api-key'
   BINANCE_SECRET_KEY='your-secret-key'
   ```

2. Configure trading parameters and risk management settings in `config.py`.

## Trading Strategies

This project implements two distinct trading strategies, leveraging technical analysis indicators to make informed trading decisions in the cryptocurrency market. Each strategy is encapsulated in its own script within the `strategies/` directory.

### Strategy 1: RSI and Moving Average

- **File**: `rsi_ma_strategy.py`
- **Indicators Used**:
  - **Relative Strength Index (RSI)**: A momentum oscillator that helps identify overbought and oversold conditions. Set to a 14-period standard for cryptocurrencies.
  - **Exponential Moving Averages (EMAs)**: Utilizes short-term (9-period) and long-term (21-period) EMAs to determine market trends.
- **Signals**:
  - **Buy**: Triggered when RSI crosses above 30 (indicating potential reversal from oversold conditions) and the short-term EMA crosses above the long-term EMA (signifying an uptrend).
  - **Sell**: Triggered when RSI crosses below 70 (indicating potential reversal from overbought conditions) and the short-term EMA crosses below the long-term EMA (signifying a downtrend).

### Strategy 2: Bollinger Bands and RSI

- **File**: `bollinger_rsi_strategy.py`
- **Indicators Used**:
  - **Bollinger Bands**: Utilizes a 20-period moving average with 2 standard deviations to identify market volatility and potential overbought/oversold conditions.
  - **RSI**: As described in Strategy 1.
- **Signals**:
  - **Buy**: Triggered when the price touches or goes below the lower Bollinger Band, and the RSI is near or below 30, indicating oversold conditions.
  - **Sell**: Triggered when the price touches or goes above the upper Bollinger Band, and the RSI is near or above 70, indicating overbought conditions.

Both strategies are designed to automate decision-making in cryptocurrency trading by analyzing market trends and momentum. Users can leverage these scripts to experiment with different trading setups and tailor them according to their risk tolerance and market observations.

## Troubleshooting

If you encounter any issues, please check the [GitHub issues page](https://github.com/blutbad33/MscFE-Capstone-Project-4538/new/main?readme=1) for solutions or to report a new issue.

## Maintainers

- [Sydney Ampaire](https://github.com/blutbad33/)
- 
```
