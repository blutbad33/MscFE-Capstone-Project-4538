import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore

# Here's where you load trade results
df = pd.read_csv('trade_results.csv')
df['Date/Time of Trade'] = pd.to_datetime(df['Date/Time of Trade'])
df['Week'] = df['Date/Time of Trade'].dt.isocalendar().week

# These are the functions to calculate various metrics needed
def analyze_trades(data):
    num_trades = len(data)
    num_profit_trades = len(data[data['Profit/Loss'] > 0])
    num_loss_trades = len(data[data['Profit/Loss'] < 0])
    gross_profit = data[data['Profit/Loss'] > 0]['Profit/Loss'].sum()
    gross_loss = data[data['Profit/Loss'] < 0]['Profit/Loss'].sum()
    max_consecutive_wins = (data['Profit/Loss'] > 0).astype(int).groupby(data['Profit/Loss'].le(0).cumsum()).cumsum().max()
    max_consecutive_profit = data['Profit/Loss'].groupby(data['Profit/Loss'].le(0).cumsum()).cumsum().max()
    num_trades_per_week = data.groupby('Week').size().mean()
    num_long_trades = len(data[data['Trade Type'] == 'Buy'])
    num_short_trades = len(data[data['Trade Type'] == 'Sell'])
    drawdown = (data['Cumulative Profit/Loss'].cummax() - data['Cumulative Profit/Loss']).max()

    # Here we calculate additional metrics like Sharpe ratio, Time weighted Return, Standard deviation, Z-score
    daily_returns = data['Profit/Loss'].pct_change()
    sharpe_ratio = daily_returns.mean() / daily_returns.std() * np.sqrt(252)
    time_weighted_return = np.prod(1 + daily_returns) - 1
    std_deviation = daily_returns.std()
    z_score = zscore(daily_returns)[-1]
    
    return {
        'Number of Trades': num_trades,
        'Number of Profit Trades': num_profit_trades,
        'Number of Loss Trades': num_loss_trades,
        'Gross Profit': gross_profit,
        'Gross Loss': gross_loss,
        'Max Consecutive Wins': max_consecutive_wins,
        'Max Consecutive Profit': max_consecutive_profit,
        'Sharpe Ratio': sharpe_ratio,
        'Time Weighted Return': time_weighted_return,
        'Standard Deviation': std_deviation,
        'Z-score': z_score,
        'Number of Trades per Week': num_trades_per_week,
        'Number of Long Trades': num_long_trades,
        'Number of Short Trades': num_short_trades,
        'Drawdown %': drawdown / (drawdown + data['Cumulative Profit/Loss'].max()) * 100
    }

# Analysis for each strategy
for strategy in df['Strategy Identifier'].unique():
    strategy_data = df[df['Strategy Identifier'] == strategy]
    metrics = analyze_trades(strategy_data)
    print(f"Metrics for {strategy}:")
    for metric, value in metrics.items():
        print(f"{metric}: {value}")

    # Plotting Graphs
    # Account balance growth
    plt.figure(figsize=(10, 6))
    strategy_data['Cumulative Profit/Loss'].plot(title=f'Account Balance Growth - {strategy}')
    plt.xlabel('Date')
    plt.ylabel('Balance')
    plt.show()

    # Drawdown in %
    drawdown = (strategy_data['Cumulative Profit/Loss'].cummax() - strategy_data['Cumulative Profit/Loss'])
    drawdown_pct = drawdown / (drawdown + strategy_data['Cumulative Profit/Loss'].max()) * 100
    plt.figure(figsize=(10, 6))
    drawdown_pct.plot(title=f'Drawdown in % - {strategy}')
    plt.xlabel('Date')
    plt.ylabel('Drawdown %')
    plt.show()
