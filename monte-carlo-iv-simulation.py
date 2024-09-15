import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Step 1: Define parameters and retrieve options prices from Yahoo Finance
def get_options_prices(ticker='AAPL', option_type='call', expiration_date=None):
    # Fetch the stock ticker object
    stock = yf.Ticker(ticker)

    # Get the expiration dates for options
    expiration_dates = stock.options
    if expiration_date is None:
        expiration_date = expiration_dates[0]  # Default to the nearest expiration date
    
    # Fetch the option chain for the specified expiration date
    option_chain = stock.option_chain(expiration_date)
    
    # Get the option prices based on the type ('call' or 'put')
    if option_type == 'call':
        option_prices = option_chain.calls['lastPrice']
    elif option_type == 'put':
        option_prices = option_chain.puts['lastPrice']
    else:
        raise ValueError("Invalid option type. Choose either 'call' or 'put'.")

    return option_prices.mean()  # Return the average of the option prices

def get_initial_IV(ticker='AAPL'):
    # Placeholder for IV retrieval, using options prices as a proxy for now
    option_price = get_options_prices(ticker)
    return 0.2  # Example IV of 20%, can be adjusted or replaced with actual IV retrieval

# Step 2: Monte Carlo simulation for asset price movements
def monte_carlo_simulation(initial_IV, current_price, num_simulations=10000, time_horizon=1):
    simulated_price_changes = []

    for _ in range(num_simulations):
        # Generate a random move from a normal distribution
        random_move = np.random.normal(loc=0, scale=initial_IV)
        # Calculate the new price based on the random movement
        new_price = current_price * np.exp(random_move * np.sqrt(time_horizon))
        simulated_price_changes.append(new_price)

    return simulated_price_changes

# Step 3: Calculate implied moves based on Monte Carlo simulations
def calculate_implied_moves(simulated_price_changes):
    # Calculate the standard deviation of the simulated price changes
    price_changes_std = np.std(simulated_price_changes)
    
    # Calculate 1/2/3 standard deviation moves
    implied_move_1STD = 1 * price_changes_std
    implied_move_2STD = 2 * price_changes_std
    implied_move_3STD = 3 * price_changes_std

    return implied_move_1STD, implied_move_2STD, implied_move_3STD

# Optional: Plot the distribution of simulated prices
def plot_simulated_prices(simulated_price_changes):
    plt.hist(simulated_price_changes, bins=50, alpha=0.75, color='blue')
    plt.title("Distribution of Simulated Asset Prices")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.show()

# Main function to run the Monte Carlo simulation and calculate implied moves
def main():
    ticker = 'AAPL'  # Example stock symbol (Apple)
    
    # Fetch current stock price using Yahoo Finance
    stock = yf.Ticker(ticker)
    current_price = stock.history(period="1d")['Close'].iloc[-1]

    # Step 1: Get initial Implied Volatility (IV)
    initial_IV = get_initial_IV(ticker)

    # Step 2: Run Monte Carlo simulation for price movements
    num_simulations = 10000  # Define the number of simulations
    time_horizon = 1  # Time horizon for the simulation (1 day)
    simulated_price_changes = monte_carlo_simulation(initial_IV, current_price, num_simulations, time_horizon)

    # Step 3: Calculate the implied moves (1, 2, 3 standard deviation moves)
    implied_move_1STD, implied_move_2STD, implied_move_3STD = calculate_implied_moves(simulated_price_changes)

    # Step 4: Print the results
    print(f"Current Price: {current_price:.2f}")
    print(f"1 STD Implied Move: {implied_move_1STD:.2f}")
    print(f"2 STD Implied Move: {implied_move_2STD:.2f}")
    print(f"3 STD Implied Move: {implied_move_3STD:.2f}")

    # Step 5: (Optional) Plot the simulated price changes
    plot_simulated_prices(simulated_price_changes)

if __name__ == "__main__":
    main()
