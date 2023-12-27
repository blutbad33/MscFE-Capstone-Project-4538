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
    return trade_size

def simulate_trades(data, strategy_name, pair, initial_capital, trade_results):
    capital = initial_capital
    cumulative_pnl = initial_capital  # Start with initial capital
    entry_price = None
    entry_time = None

    for i in range(1, len(data)):
        timestamp = data['timestamp'].iloc[i]
        close_price = data['close'].iloc[i]
        exit_price = None
        profit_loss = 0
        position_status = 'Open' if entry_price is not None else 'Closed'

        if data['Buy'].iloc[i] and capital > 0 and not entry_price:
            entry_price = close_price
            stop_loss_price = entry_price - (entry_price * config.STOP_LOSS_PERCENTAGE)
            trade_size = calculate_trade_size(cumulative_pnl, entry_price, stop_loss_price)
            entry_time = timestamp
            capital -= trade_size * entry_price  # Update capital to reflect the position
            position_status = 'Open'
        elif (data['Sell'].iloc[i] or (entry_time and timestamp - entry_time > timedelta(hours=24))) and entry_price is not None:
            exit_price = close_price
            profit_loss = trade_size * (exit_price - entry_price)
            cumulative_pnl += profit_loss
            capital += trade_size * exit_price  # Update capital to reflect closing the position
            position_status = 'Closed'

        if exit_price is not None:
            trade_duration = (timestamp - entry_time).total_seconds() / 3600 if entry_time else 0
            risk_per_trade = config.RISK_PER_TRADE
            trade_results.append({
                'Date/Time of Trade': entry_time.strftime("%m/%d/%Y %H:%M") + ' - ' + timestamp.strftime("%m/%d/%Y %H:%M") if entry_time else '',
                'Trade Duration (hrs)': trade_duration,
                'Strategy Identifier': strategy_name,
                'Trading Pair': pair,
                'Trade Size': trade_size if trade_size is not None else 0,
                'Risk Per Trade': risk_per_trade,
                'Entry Price': entry_price,
                'Exit Price': exit_price,
                'Profit/Loss': profit_loss,
                'Cumulative Profit/Loss': cumulative_pnl,
                'Position Status': position_status
            })
            entry_price = None  # Reset entry price for the next trade
            trade_size = None  # Reset trade size for the next trade

    return capital

def main():
    trading_pairs = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT']
    trade_results = []
    initial_capital = config.INITIAL_CAPITAL

    for pair in trading_pairs:
        data = load_data(pair)
        simulate_trades(rsi_ma_strategy(data.copy()), 'RSI_MA', pair, initial_capital, trade_results)
        simulate_trades(bollinger_rsi_strategy(data.copy()), 'Bollinger_RSI', pair, initial_capital, trade_results)

    # Save trade results to CSV
    trade_results_df = pd.DataFrame(trade_results)
    trade_results_df.to_csv('trade_results.csv', index=False)

    # Organize trade results by timestamp and recalculate 'Cumulative Profit/Loss'
    trade_results_df['Date/Time of Trade'] = pd.to_datetime(trade_results_df['Date/Time of Trade'].str.split(' - ').str[0])
    organized_trade_results_df = trade_results_df.sort_values(by='Date/Time of Trade')
    organized_trade_results_df['Cumulative Profit/Loss'] = organized_trade_results_df['Profit/Loss'].cumsum() + initial_capital
    organized_trade_results_df.to_csv('trade_results_Organised.csv', index=False)

if __name__ == "__main__":
    main()
