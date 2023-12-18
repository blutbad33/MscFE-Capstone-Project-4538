import pandas as pd
import os

# Import strategies
from strategies.rsi_ma_strategy import rsi_ma_strategy
from strategies.bollinger_rsi_strategy import bollinger_rsi_strategy

# Initial setup
initial_capital = 10000
trading_pairs = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT']
trade_results = []

# Load Crypto Pairs
def load_data(pair):
    filename = f'data/{pair}_data.csv'
    return pd.read_csv(filename, parse_dates=['timestamp'])

# Define Simulate Trade of the Technical Analysis Strategy
def simulate_trades(data, strategy_name, pair, initial_capital):
    capital = initial_capital
    position = 0
    cumulative_pnl = 0

    for i in range(1, len(data)):
        timestamp = data['timestamp'].iloc[i]
        close_price = data['close'].iloc[i]
        trade_size = 0
        entry_price = 0
        exit_price = 0
        profit_loss = 0
        position_status = 'Hold'

        if data['Buy'].iloc[i] and capital > 0:
            trade_size = capital / close_price
            entry_price = close_price
            position = trade_size
            capital = 0
            position_status = 'Open'
        elif data['Sell'].iloc[i] and position > 0:
            exit_price = close_price
            capital = position * close_price
            profit_loss = (exit_price - entry_price) * trade_size
            cumulative_pnl += profit_loss
            position = 0
            trade_size = 0
            position_status = 'Close'

        if position_status in ['Open', 'Close']:
            trade_results.append({
                'Date/Time of Trade': timestamp,
                'Strategy Identifier': strategy_name,
                'Trading Pair': pair,
                'Trade Type': 'Buy' if position_status == 'Open' else 'Sell',
                'Trade Size': trade_size,
                'Entry Price': entry_price,
                'Exit Price': exit_price,
                'Profit/Loss': profit_loss,
                'Cumulative Profit/Loss': cumulative_pnl,
                'Position Status': position_status
            })

    final_capital = capital + position * data['close'].iloc[-1]
    return final_capital


def main():
    for pair in trading_pairs:
        data = load_data(pair)

        # Apply and simulate RSI and MA strategy
        strategy_data = rsi_ma_strategy(data.copy())
        simulate_trades(strategy_data, 'RSI_MA', pair, initial_capital)

        # Apply and simulate Bollinger Bands and RSI strategy
        strategy_data = bollinger_rsi_strategy(data.copy())
        simulate_trades(strategy_data, 'Bollinger_RSI', pair, initial_capital)

    # Save trade results to CSV
    pd.DataFrame(trade_results).to_csv('trade_results.csv', index=False)

if __name__ == "__main__":
    main()
