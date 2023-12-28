import pandas as pd
from strategies.rsi_ma_strategy import rsi_ma_strategy
from strategies.bollinger_rsi_strategy import bollinger_rsi_strategy
from datetime import timedelta
import config

# Function to load data for each trading pair
def load_data(pair):
    filename = f'{pair}_data.csv'
    return pd.read_csv(filename, parse_dates=['timestamp'])

# Function to calculate trade size
def calculate_trade_size(cumulative_profit, entry_price, stop_loss_price):
    dollar_risk = cumulative_profit * config.RISK_PER_TRADE
    price_risk_per_unit = abs(entry_price - stop_loss_price)
    return dollar_risk / price_risk_per_unit

# Function to simulate trades based on a strategy
def simulate_trades(data, strategy_name, pair, initial_capital, trade_results):
    capital = initial_capital
    cumulative_pnl = initial_capital
    entry_price = None
    entry_time = None

    for i in range(1, len(data)):
        timestamp = data['timestamp'].iloc[i]
        close_price = data['close'].iloc[i]
        exit_price = None
        profit_loss = 0

        if data['Buy'].iloc[i] and capital > 0 and not entry_price:
            entry_price = close_price
            stop_loss_price = entry_price - (entry_price * config.STOP_LOSS_PERCENTAGE)
            trade_size = calculate_trade_size(cumulative_pnl, entry_price, stop_loss_price)
            entry_time = timestamp
            capital -= trade_size * entry_price
        elif (data['Sell'].iloc[i] or (entry_time and timestamp - entry_time > timedelta(hours=24))) and entry_price is not None:
            exit_price = close_price
            profit_loss = trade_size * (exit_price - entry_price)
            cumulative_pnl += profit_loss
            capital += trade_size * exit_price

        if exit_price is not None:
            risk_per_trade = config.RISK_PER_TRADE
            trade_results.append({
                'Date/Time of Trade': entry_time.strftime("%m/%d/%Y %H:%M") + ' - ' + timestamp.strftime("%m/%d/%Y %H:%M"),
                'Trade Duration (hrs)': (timestamp - entry_time).total_seconds() / 3600 if entry_time else 0,
                'Strategy Identifier': strategy_name,
                'Trading Pair': pair,
                'Trade Size': trade_size,
                'Risk Per Trade': risk_per_trade,
                'Entry Price': entry_price,
                'Exit Price': exit_price,
                'Profit/Loss': profit_loss,
                'Cumulative Profit/Loss': cumulative_pnl
            })
            entry_price = None

    return capital

# Function to calculate daily returns
def calculate_daily_returns(trade_results_df):
    try:
        print("Calculating daily returns...")
        # Split the 'Date/Time of Trade' column and convert the start time to datetime
        trade_results_df['Start Time'] = pd.to_datetime(trade_results_df['Date/Time of Trade'].str.split(' - ').str[0], format='%m/%d/%Y %H:%M')

        trade_results_df['Date'] = trade_results_df['Start Time'].dt.date
        strategies = trade_results_df['Strategy Identifier'].unique()
        daily_returns = pd.DataFrame()

        for strategy in strategies:
            strategy_data = trade_results_df[trade_results_df['Strategy Identifier'] == strategy]
            strategy_daily = strategy_data.groupby('Date')['Profit/Loss'].sum()
            daily_returns[strategy] = strategy_daily

        combined_daily = trade_results_df.groupby('Date')['Profit/Loss'].sum()
        daily_returns['Combined'] = combined_daily

        daily_returns_pct = daily_returns.pct_change() * 100
        daily_returns_pct.reset_index(inplace=True)
        daily_returns_pct.rename(columns={'Date': 'Day/Date'}, inplace=True)
        return daily_returns_pct
    except Exception as e:
        print(f"Error in calculate_daily_returns: {e}")
        return pd.DataFrame()

# Main function to run the trading simulation
def main():
    trading_pairs = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT']
    trade_results = []

    for pair in trading_pairs:
        data = load_data(pair)
        simulate_trades(rsi_ma_strategy(data.copy()), 'RSI_MA', pair, config.INITIAL_CAPITAL, trade_results)
        simulate_trades(bollinger_rsi_strategy(data.copy()), 'Bollinger_RSI', pair, config.INITIAL_CAPITAL, trade_results)

    trade_results_df = pd.DataFrame(trade_results)
    trade_results_df.to_csv('trade_results.csv', index=False)

    organized_trade_results_df = trade_results_df.sort_values(by='Date/Time of Trade')
    organized_trade_results_df['Cumulative Profit/Loss'] = organized_trade_results_df['Profit/Loss'].cumsum() + config.INITIAL_CAPITAL
    organized_trade_results_df.to_csv('trade_results_Organised.csv', index=False)

    daily_returns_df = calculate_daily_returns(organized_trade_results_df)
    daily_returns_df.to_csv('daily_returns.csv', index=False)

if __name__ == "__main__":
    main()
