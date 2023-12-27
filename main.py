import pandas as pd
from strategies.rsi_ma_strategy import rsi_ma_strategy
from strategies.bollinger_rsi_strategy import bollinger_rsi_strategy
from datetime import timedelta
import config

# Load Crypto Pairs
def load_data(pair):
    filename = f'{pair}_data.csv'
    return pd.read_csv(filename, parse_dates=['timestamp'])

def calculate_trade_size(cumulative_profit, entry_price, stop_loss_price):
    dollar_risk = cumulative_profit * config.RISK_PER_TRADE
    price_risk_per_unit = abs(entry_price - stop_loss_price)
    trade_size = dollar_risk / price_risk_per_unit
    return trade_size, config.RISK_PER_TRADE

def simulate_trades(data, strategy_name, pair, initial_capital, trade_results):
    capital = initial_capital
    cumulative_pnl = initial_capital
    entry_price = None
    entry_time = None
    trade_size = None
    risk_per_trade = None

    for i in range(1, len(data)):
        timestamp = data['timestamp'].iloc[i]
        close_price = data['close'].iloc[i]
        exit_price = None
        profit_loss = 0

        if data['Buy'].iloc[i] and capital > 0 and not entry_price:
            entry_price = close_price
            stop_loss_price = entry_price - (initial_capital * config.STOP_LOSS_PERCENTAGE)
            trade_size, risk_per_trade = calculate_trade_size(cumulative_pnl, entry_price, stop_loss_price)
            entry_time = timestamp
            capital -= trade_size * entry_price

        if (data['Sell'].iloc[i] or (entry_time and timestamp - entry_time >= timedelta(hours=24))) and entry_price is not None:
            exit_price = close_price
            profit_loss = trade_size * (exit_price - entry_price) if trade_size is not None else 0
            cumulative_pnl += profit_loss
            capital += trade_size * exit_price if trade_size is not None else 0

        if exit_price is not None or (entry_time and timestamp - entry_time >= timedelta(hours=24)):
            trade_duration = (timestamp - entry_time).total_seconds() / 3600 if entry_time else 0
            trade_results.append({
                'Date/Time of Trade': entry_time.strftime("%m/%d/%Y %H:%M") + ' - ' + timestamp.strftime("%m/%d/%Y %H:%M"),
                'Trade Duration (hrs)': trade_duration,
                'Strategy Identifier': strategy_name,
                'Trading Pair': pair,
                'Trade Size': trade_size if trade_size is not None else 0,
                'Risk Per Trade': risk_per_trade if risk_per_trade is not None else 0,
                'Entry Price': entry_price,
                'Exit Price': exit_price if exit_price is not None else 0,
                'Profit/Loss': profit_loss,
                'Cumulative Profit/Loss': cumulative_pnl,
                'Position Status': 'Closed'
            })
            entry_price = None  # Reset for the next trade
            trade_size = None  # Reset for the next trade
            risk_per_trade = None  # Reset for the next trade

    return capital

def main():
    trading_pairs = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT']
    trade_results = []
    initial_capital = config.INITIAL_CAPITAL

    for pair in trading_pairs:
        data = load_data(pair)

        # Apply and simulate RSI and MA strategy
        simulate_trades(rsi_ma_strategy(data.copy()), 'RSI_MA', pair, initial_capital, trade_results)

        # Apply and simulate Bollinger Bands and RSI strategy
        simulate_trades(bollinger_rsi_strategy(data.copy()), 'Bollinger_RSI', pair, initial_capital, trade_results)

    # Save trade results to CSV and sort by trade date and time
    trade_results_df = pd.DataFrame(trade_results)
    trade_results_df['Date/Time of Trade'] = pd.to_datetime(trade_results_df['Date/Time of Trade'].str.split(' - ').str[0])
    trade_results_df.sort_values(by='Date/Time of Trade', inplace=True)
    trade_results_df.to_csv('trade_results.csv', index=False)

if __name__ == "__main__":
    main()
