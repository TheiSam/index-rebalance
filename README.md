## __Index Fund Rebalancing Simulator__
This project simulates index fund rebalancing using mock company market cap and price data across two different dates.

## __Prerequisites__
Install the required modules using:
``pip3 install -r requirements.txt``

## __Usage__
Run the script with:
``python3 src/index_rebalance.py``

* Input data can be found in the data/ folder
* Results will be saved in the results/ folder. 
The script outputs the following results as CSV files:
- Initial portfolio (Date 1)
- New portfolio (Date 2)
- Equities bought during rebalancing
- Equities sold during rebalancing

## __Testing__
Run the unit tests with:
``pytest tests/``

## __Code Overview__
* `src/helpers.py` -> functions for loading data, calculating weights, merging datasets.
* `src/index_rebalance.py` -> runs the end-to-end rebalance process which:
    1) Loads input data
    2) Determines desired index portfolio at the given dates
    3) Identify buy/sell actions
    4) Save results

## __Suggestions for Future Improvements__

1) Code Improvements
    * Add more unit tests for edge cases (e.g. missing data, negative prices, duplicates).
    * Handle fractional shares or rounding consistently.
2) Data Improvements
    * Include fees, dividends and corporate actions (e.g. stock splits) for a more realistic simulation.
    * Use higher-frequency data.
    * Include international stocks with FX rates.
3) Feature Improvements
    * Automate rebalancing over multiple dates (more than 2).
    * Allow configurable thresholds and indexes.
    * Visualisation of portfolio weights and performance over time.