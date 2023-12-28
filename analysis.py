import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore

# Load trade results
df = pd.read_csv('trade_results_Organised.csv')
df['Date/Time of Trade'] = pd.to_datetime(df['Date/Time of Trade'])
initial_capital = 10000  # Assuming initial capital is 10,000
risk_free_return = 0.01  # 1% risk-free return

# Function to calculate various metrics
def analyze_trades(data):
    num_trades = len(data)
    num_profit_trades = len(data[data['Profit/Loss'] > 0])
    num_loss_trades = len(data[data['Profit/Loss'] < 0])
    gross_profit = data[data['Profit/Loss'] > 0]['Profit/Loss'].sum()
    gross_loss = data[data['Profit/Loss'] < 0]['Profit/Loss'].sum()
    account_balance = data['Cumulative Profit/Loss'].iloc[-1] + initial_capital
    roi = (account_balance - initial_capital) / initial_capital * 100

    profit_trade_margin = num_profit_trades / num_trades * 100 if num_trades > 0 else 0
    loss_trade_margin = num_loss_trades / num_trades * 100 if num_trades > 0 else 0

    daily_returns = data['Profit/Loss'].pct_change().dropna()
    mean_return = np.mean(daily_returns)
    sharpe_ratio = (mean_return - risk_free_return) / np.std(daily_returns) * np.sqrt(252)
    std_deviation = np.std(daily_returns)

    return {
        'Number of Trades': num_trades,
        'Number of Profit Trades': num_profit_trades,
        'Number of Loss Trades': num_loss_trades,
        'Profit Trade Margin (%)': profit_trade_margin,
        'Loss Trade Margin (%)': loss_trade_margin,
        'Gross Profit': gross_profit,
        'Gross Loss': gross_loss,
        'Account Balance': account_balance,
        'ROI (%)': roi,
        'Mean Return': mean_return,
        'Sharpe Ratio': sharpe_ratio,
        'Standard Deviation': std_deviation
    }

# Compare strategies
strategy_metrics = {}
strategies = df['Strategy Identifier'].unique()
for strategy in strategies:
    strategy_data = df[df['Strategy Identifier'] == strategy]
    metrics = analyze_trades(strategy_data)
    strategy_metrics[strategy] = metrics

# Analyze combined performance
combined_data = df.copy()
combined_metrics = analyze_trades(combined_data)
strategy_metrics['Combined'] = combined_metrics

# Save metrics to CSV
analysis_df = pd.DataFrame(strategy_metrics)
analysis_df.to_csv('analysis.csv')

# Plotting graphs for each strategy and combined strategy
for strategy in strategies.tolist() + ['Combined']:
    strategy_data = combined_data if strategy == 'Combined' else df[df['Strategy Identifier'] == strategy]
    
    # Account balance growth
    plt.figure(figsize=(10, 6))
    strategy_data['Cumulative Profit/Loss'].plot(title=f'Account Balance Growth - {strategy}')
    plt.xlabel('Years')
    plt.ylabel('Balance')
    plt.xticks(ticks=np.arange(strategy_data['Date/Time of Trade'].min().year, strategy_data['Date/Time of Trade'].max().year + 1, 1))
    plt.savefig(f'account_balance_growth_{strategy}.png')
    plt.close()

    # Drawdown in %
    drawdown = (strategy_data['Cumulative Profit/Loss'].cummax() - strategy_data['Cumulative Profit/Loss'])
    drawdown_pct = drawdown / strategy_data['Cumulative Profit/Loss'].cummax() * 100
    plt.figure(figsize=(10, 6))
    drawdown_pct.plot(title=f'Drawdown in % - {strategy}')
    plt.xlabel('Years')
    plt.ylabel('Drawdown %')
    plt.ylim(-20, 35)  # Set y-axis limits
    plt.xticks(ticks=np.arange(strategy_data['Date/Time of Trade'].min().year, strategy_data['Date/Time of Trade'].max().year + 1, 1))
    plt.savefig(f'drawdown_{strategy}.png')
    plt.close()
