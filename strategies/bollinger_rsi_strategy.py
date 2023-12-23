import pandas as pd
import os
from strategies.rsi_ma_strategy import rsi_ma_strategy
from strategies.bollinger_rsi_strategy import bollinger_rsi_strategy

# Initial setup
initial_capital = 10000
trading_pairs = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT']
trade_results = []

# Load Crypto Pairs
def load_data(pair):
    filename = f'{pair}_data.csv'
    return pd.read_csv(filename, parse_dates=['timestamp'])

def simulate_trades(data, strategy_name, pair, initial_capital):
    capital = initial_capital
    position = 0
    cumulative_pnl = initial_capital  # Start with initial capital
    entry_price = None
    entry_time = None
    trade_size = 0

    for i in range(1, len(data)):
        timestamp = data['timestamp'].iloc[i]
        close_price = data['close'].iloc[i]
        exit_price = None
        profit_loss = 0
        position_status = 'Closed'  # Default to 'Closed'

        if data['Buy'].iloc[i] and capital > 0 and not position:
            trade_size = capital / close_price
            entry_price = close_price
            entry_time = timestamp
            position = trade_size
            capital = 0
        elif data['Sell'].iloc[i] and position > 0 and entry_price is not None:
            exit_price = close_price
            profit_loss = trade_size * (exit_price - entry_price)
            cumulative_pnl += profit_loss
            position = 0
            trade_size = 0
            trade_time = f'{entry_time.strftime("%d/%m/%Y %H:%M")} - {timestamp.strftime("%d/%m/%Y %H:%M")}'
            trade_results.append({
                'Date/Time of Trade': trade_time,
                'Strategy Identifier': strategy_name,
                'Trading Pair': pair,
                'Trade Size': trade_size,
                'Entry Price': entry_price,
                'Exit Price': exit_price,
                'Profit/Loss': profit_loss,
                'Cumulative Profit/Loss': cumulative_pnl,
                'Position Status': position_status
            })

    final_capital = capital + position * data['close'].iloc[-1] if position > 0 else capital
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
