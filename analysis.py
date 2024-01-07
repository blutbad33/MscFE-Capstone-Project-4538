import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import zscore

# Load trade results
df = pd.read_csv('trade_results_Organised.csv')
daily_returns_df = pd.read_csv('daily_returns.csv')
daily_returns_df['Day/Date'] = pd.to_datetime(daily_returns_df['Day/Date'], format = '%d/%m/%Y')

# Function to convert string of returns to a list of floats
def convert_to_floats(return_string):
    try:
        return [float(item) for item in return_string.split()]
    except ValueError:
        return np.nan

# Load and process daily returns
daily_returns_df = pd.read_csv('daily_returns.csv')
daily_returns_df['Day/Date'] = pd.to_datetime(daily_returns_df['Day/Date'], format = '%d/%m/%Y')

# Convert return data to numeric format
for column in daily_returns_df.columns:
    if column != 'Day/Date':
        daily_returns_df[column] = pd.to_numeric(daily_returns_df[column], errors='coerce')

# Function to calculate various metrics
def analyze_trades(data, daily_returns):
    if data.empty:
        return {
            'Number of Trades': 0,
            'Number of Profit Trades': 0,
            'Number of Loss Trades': 0,
            'Profit Trade Margin (%)': 0,
            'Loss Trade Margin (%)': 0,
            'Gross Profit': 0,
            'Gross Loss': 0,
            'Account Balance': 10000,  # Initial capital
            'ROI (%)': 0,
            'Mean Return': 0,
            'Sharpe Ratio': 0,
            'Standard Deviation': 0
        }
    num_trades = len(data)
    num_profit_trades = len(data[data['Profit/Loss'] > 0])
    num_loss_trades = len(data[data['Profit/Loss'] < 0])
    gross_profit = data[data['Profit/Loss'] > 0]['Profit/Loss'].sum()
    gross_loss = data[data['Profit/Loss'] < 0]['Profit/Loss'].sum()
    account_balance = data['Cumulative Profit/Loss'].iloc[-1] + 10000  # Adding initial capital
    roi = (account_balance - 10000) / 10000 * 100  # Calculating ROI

    profit_trade_margin = num_profit_trades / num_trades * 100 if num_trades > 0 else 0
    loss_trade_margin = num_loss_trades / num_trades * 100 if num_trades > 0 else 0

    # Calculating mean return, Sharpe ratio, and standard deviation from daily returns
    mean_return = daily_returns.mean()
    std_deviation = daily_returns.std()
    sharpe_ratio = mean_return / std_deviation * np.sqrt(252) if std_deviation != 0 else None

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

# Function for Monte Carlo Simulation
def monte_carlo_simulation(data, num_simulations=1000):
    if data.empty:
        return {"Monte Carlo Mean Ending Balance": 0}

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

# Function for Risk of Ruin Analysis
def risk_of_ruin(data):
    losing_trades = data[data['Profit/Loss'] < 0]
    win_rate = 1 - len(losing_trades) / len(data) if len(data) > 0 else 0
    average_loss = losing_trades['Profit/Loss'].mean() if not losing_trades.empty else 0
    risk_of_ruin = np.power(average_loss / data['Cumulative Profit/Loss'].max(), len(data)) if average_loss < 0 else 0
    return {"Risk of Ruin": risk_of_ruin}

# Analyze strategies using daily returns
strategy_metrics = {}
strategies = ['RSI_MA', 'Bollinger_RSI', 'Combined']
for strategy in strategies:
    strategy_data = df[df['Strategy Identifier'] == strategy.strip()]
    strategy_daily_returns = daily_returns_df[strategy].dropna()
    metrics = analyze_trades(strategy_data, strategy_daily_returns)
    strategy_metrics[strategy.strip()] = metrics

# Analyze combined performance
combined_data = df.copy()
combined_daily_returns = daily_returns_df['Combined'].dropna()
combined_metrics = analyze_trades(combined_data, combined_daily_returns)
strategy_metrics['Combined'] = combined_metrics

# After calculating strategy_metrics, create an index list
index_list = ['Number of Trades', 'Number of Profit Trades', 'Number of Loss Trades', 
              'Profit Trade Margin (%)', 'Loss Trade Margin (%)', 'Gross Profit', 
              'Gross Loss', 'Account Balance', 'ROI (%)', 'Mean Return', 
              'Sharpe Ratio', 'Standard Deviation']

# Create a DataFrame using strategy_metrics and the custom index
analysis_df = pd.DataFrame(strategy_metrics, index=index_list)

# Save metrics to CSV
analysis_df.to_csv('analysis.csv')

# Risk of Ruin and Monte Carlo Analysis
risk_ruin_monte_carlo_df = pd.DataFrame(index=strategies + [' Combined '])
for strategy in strategies + [' Combined ']:
    if strategy == ' Combined ':
        strategy_data = combined_data
    elif strategy == ' RSI_MA ':
        strategy_data = df[df['Strategy Identifier'] == 'RSI_MA']
    elif strategy == ' Bollinger_RSI ':
        strategy_data = df[df['Strategy Identifier'] == 'Bollinger_RSI']

    # Debug: Print the data for strategy
    print(f"Strategy: {strategy}")
    print(strategy_data.head())  # Print the first few rows of data

    # Calculate Risk of Ruin and Monte Carlo Mean Ending Balance
    risk_of_ruin_result = risk_of_ruin(strategy_data)
    monte_carlo_result = monte_carlo_simulation(strategy_data)
    
    # Debug: Print intermediate results
    print(f"Risk of Ruin Result: {risk_of_ruin_result}")
    print(f"Monte Carlo Result: {monte_carlo_result}")
    
    risk_ruin_monte_carlo_df.loc[strategy, 'Risk of Ruin'] = risk_of_ruin(strategy_data)["Risk of Ruin"]
    risk_ruin_monte_carlo_df.loc[strategy, 'Monte Carlo Mean Ending Balance'] = monte_carlo_simulation(strategy_data)["Monte Carlo Mean Ending Balance"]

risk_ruin_monte_carlo_df.to_csv('risk_ruin_monte_carlo_analysis.csv')
  
#Plotting
df['Start Time'] = pd.to_datetime(df['Date/Time of Trade'].str.split(' - ').str[0], format='%m/%d/%Y %H:%M')
df.set_index('Start Time', inplace=True)

# Define the data for each strategy
rsi_ma_data = df[df['Strategy Identifier'] == 'RSI_MA']
bollinger_rsi_data = df[df['Strategy Identifier'] == 'Bollinger_RSI']

# Function to calculate drawdown in %
def calculate_drawdown(data):
    drawdown = (data['Cumulative Profit/Loss'].cummax() - data['Cumulative Profit/Loss'])
    drawdown_pct = drawdown / data['Cumulative Profit/Loss'].cummax() * 100
    return drawdown_pct

# Plot Account Balance Growth for each strategy and combined
plt.figure(figsize=(10, 6))
plt.plot(df['Cumulative Profit/Loss'], label='Combined', color='blue')
plt.plot(rsi_ma_data['Cumulative Profit/Loss'], label='RSI_MA', color='green')
plt.plot(bollinger_rsi_data['Cumulative Profit/Loss'], label='Bollinger_RSI', color='red')
plt.title('Account Balance Growth')
plt.xlabel('Date')
plt.ylabel('Balance')
plt.legend()
plt.xticks([])
plt.savefig('account_balance_growth_corrected.png')
plt.close()

# Plot Drawdown in % for each strategy and combined
plt.figure(figsize=(10, 6))
plt.plot(calculate_drawdown(df), label='Combined', color='blue')
plt.plot(calculate_drawdown(rsi_ma_data), label='RSI_MA', color='green')
plt.plot(calculate_drawdown(bollinger_rsi_data), label='Bollinger_RSI', color='red')
plt.title('Drawdown in %')
plt.xlabel('Date')
plt.ylabel('Drawdown %')
plt.legend()
plt.ylim(-20, 35)  # Set y-axis limits if necessary
plt.xticks([])
plt.savefig('drawdown_corrected.png')
plt.close()
