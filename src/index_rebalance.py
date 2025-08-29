import os
import pandas as pd
import helpers

# Given parameters
FIRST_DATE = "8/04/2025"
SECOND_DATE = "8/05/2025"
INITIAL_CAPITAL = 100000000
CUTOFF = 0.85

# Load data
script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, "..", "data", "market_capitalisation.csv")
data = pd.read_csv(data_path)

# Filter the data for the date `2025-04-08`
df = data[data["date"] == FIRST_DATE]

initial_portfolio = helpers.build_index(df, INITIAL_CAPITAL, CUTOFF)

# Filter the data for the second date (`2025-05-08`)
df2 = data[data["date"] == SECOND_DATE]

new_portfolio = helpers.build_index(df2, INITIAL_CAPITAL, CUTOFF)
portfolio_status = helpers.rebalance_portfolio(initial_portfolio, new_portfolio, df2)

# Identify equities to sell and their value
equities_sold = portfolio_status[portfolio_status["status"] == "sell"]

# Identify equities to buy
equities_bought = portfolio_status[portfolio_status["status"] == "buy"]

# Calculate the final rebalanced portfolio for Q2
final_portfolio = new_portfolio.copy()

# Clean up and save results
results_dir = os.path.join(script_dir, "..", "results")

cols_to_save_portfolio = ["date", "company", "market_cap_m", "price", "dollars_allocated", "num_shares"]
initial_portfolio[cols_to_save_portfolio].to_csv(os.path.join(results_dir, "initial_portfolio.csv"), index=False)
new_portfolio[cols_to_save_portfolio].to_csv(os.path.join(results_dir, "new_portfolio.csv"), index=False)

cols_to_save_bought = ["company", "num_shares_new", "price_new"]
equities_bought = equities_bought[cols_to_save_bought].rename(
    columns={"price_new": "price", "num_shares_new": "num_shares"}
)
equities_bought.to_csv(os.path.join(results_dir, "equities_bought.csv"), index=False)

cols_to_save_sold = ["company", "num_shares_old", "price_new", "current_value"]
equities_sold = equities_sold[cols_to_save_sold].rename(
    columns={"price_new": "price", "num_shares_old": "num_shares", "current_value": "total_value"}
)
equities_sold.to_csv(os.path.join(results_dir, "equities_sold.csv"), index=False)


'''
3. Scenarios & Real World Considerations

--- Potential Error Scenarios ---
1. Missing data:
    - 'price' or 'market_cap_m' columns contain NaN 
    - Calculations fail when trying to build index
    - If company is missing, index rebalancing will fail as the old and new portfolio cannot be merged properly
2. Incorrect datatypes:
    - 'price' or 'market_cap_m' columns stored as strings instead of numeric
    -  Calculations fail when trying to build index
3. Duplicate company entries:
    - Index may be incorrectly constructed where some companies may not make the cutoff when they should
4. Invalid data:
    - For example, negative price or market cap will result in incorrect calculations.

--- Requirements to be able to identify sources of error ---
1. Consistent schema
    - Input data must have:
        - "date","company","market_cap_m","price" columns
        - "date" and "company" must be strings and cannot be empty
        - "market_cap_m" and "price" must be numeric and positive
    - index must contain "company", "price", "num_shares"
        - "company" must be a string
        - "price" and "num_shares" must be numeric
2. Complete data
    - No missing row values in input data
3. Index portfolios must be created with the same column names


--- What may be missing from the dataset (Real world considerations) ---
1. Fees
    - Management fees and transaction costs may reduce real portfolio value
2. Weight drift
    - Weights of the portfolio companies change continuously, not just at rebalancing
3. Dividend reinvestment
    - Dividends may be reinvested, which would affect share counts and weights
4. Trading constraints
    - Fractional shares may not be allowed
5. Currency
    - If stocks are listed on international exchanges, FX fluctuations will matter.
6. Data frequency
    - Rebalancing outcomes will differ depending on whether daily closing prices are used or intraday prices.
7. Corporate actions
    - Certain corporate actions, like stock splits, will impact share counts and weights
8. Liquidity complaints
    - Trading at exactly the calculated weights and prices may not be possible.
'''






