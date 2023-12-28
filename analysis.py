import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore

# Load trade results
df = pd.read_csv('trade_results_Organised.csv')
df['Date/Time of Trade'] = pd.to_datetime(df['Date/Time of Trade'].str.split(' - ').str[0])

# Function to calculate various metrics
def analyze_trades(data):
    num_trades = len(data)
    num_profit_trades = len(data[data['Profit/Loss'] > 0])
    num_loss_trades = len(data[data['Profit/Loss'] < 0])
    gross_profit = data[data['Profit/Loss'] > 0]['Profit/Loss'].sum()
    gross_loss = data[data['Profit/Loss'] < 0]['Profit/Loss'].sum()
    account_balance = data['Cumulative Profit/Loss'].iloc[-1] + 10000  # Adding initial capital
    roi = (account_balance - 10000) / 10000 * 100  # Calculating ROI

    profit_trade_margin = num_profit_trades / num_trades * 100 if num_trades > 0 else 0
    loss_trade_margin = num_loss_trades / num_trades * 100 if num_trades > 0 else 0

    daily_returns = data['Profit/Loss'].pct_change().dropna()
    mean_return = np.mean(daily_returns)
    sharpe_ratio = (mean_return - 0.01) / np.std(daily_returns) * np.sqrt(252) if np.std(daily_returns) != 0 else None
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

# Function for Risk of Ruin Analysis
def risk_of_ruin(data):
    losing_trades = data[data['Profit/Loss'] < 0]
    win_rate = 1 - len(losing_trades) / len(data) if len(data) > 0 else 0
    average_loss = losing_trades['Profit/Loss'].mean() if not losing_trades.empty else 0
    risk_of_ruin = np.power(average_loss / data['Cumulative Profit/Loss'].max(), len(data)) if average_loss < 0 else 0
    return {"Risk of Ruin": risk_of_ruin}

# Function for Monte Carlo Simulation
def monte_carlo_simulation(data, num_simulations=1000):
    mean_return = data['Profit/Loss'].pct_change().mean()
    std_deviation = data['Profit/Loss'].pct_change().std()
    initial_balance = 10000
    simulation_results = []

    for _ in range(num_simulations):
        simulated_balance = initial_balance
        for _ in range(len(data)):
            simulated_balance *= (1 + np.random.normal(mean_return, std_deviation))
        simulation_results.append(simulated_balance)

    return {"Monte Carlo Mean Ending Balance": np.mean(simulation_results)}

# Analyze strategies
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

# Risk of Ruin and Monte Carlo Analysis
risk_ruin_monte_carlo_df = pd.DataFrame(index=strategies.tolist() + ['Combined'])
for strategy in strategies.tolist() + ['Combined']:
    strategy_data = combined_data if strategy == 'Combined' else df[df['Strategy Identifier'] == strategy]
    risk_ruin_monte_carlo_df.loc[strategy, 'Risk of Ruin'] = risk_of_ruin(strategy_data)["Risk of Ruin"]
    risk_ruin_monte_carlo_df.loc[strategy, 'Monte Carlo Mean Ending Balance'] = monte_carlo_simulation(strategy_data)["Monte Carlo Mean Ending Balance"]

risk_ruin_monte_carlo_df.to_csv('risk_ruin_monte_carlo_analysis.csv')

# Plotting graphs for each strategy and combined strategy
for strategy in strategies.tolist() + ['Combined']:
    strategy_data = combined_data if strategy == 'Combined' else df[df['Strategy Identifier'] == strategy]
    
    # Account balance growth
    plt.figure(figsize=(10, 6))
    strategy_data['Cumulative Profit/Loss'].plot(title=f'Account Balance Growth - {strategy}')
    plt.xlabel('Date')
    plt.ylabel('Balance')
    plt.xticks(ticks=pd.date_range(start=strategy_data['Date/Time of Trade'].min(), end=strategy_data['Date/Time of Trade'].max(), freq='Y').year)
    plt.savefig(f'account_balance_growth_{strategy}.png')
    plt.close()

    # Drawdown in %
    drawdown = (strategy_data['Cumulative Profit/Loss'].cummax() - strategy_data['Cumulative Profit/Loss'])
    drawdown_pct = drawdown / strategy_data['Cumulative Profit/Loss'].cummax() * 100
    plt.figure(figsize=(10, 6))
    drawdown_pct.plot(title=f'Drawdown in % - {strategy}')
    plt.xlabel('Date')
    plt.ylabel('Drawdown %')
    plt.ylim(-20, 35)  # Set y-axis limits
    plt.xticks(ticks=pd.date_range(start=strategy_data['Date/Time of Trade'].min(), end=strategy_data['Date/Time of Trade'].max(), freq='Y').year)
    plt.savefig(f'drawdown_{strategy}.png')
    plt.close()