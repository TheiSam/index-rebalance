def build_index(df, capital=100000000, cutoff=0.85):
    """
    Build an index portfolio for a given date's data.
    
    Args:
        df (pd.DataFrame): DataFrame for a single date with columns ["company", "market_cap_m", "price"]
        capital (float): Total capital to allocate
        cutoff (float): Cumulative weight threshold
        
    Returns:
        pd.DataFrame: Portfolio with weight, cumulative weight, allocation, and num_shares
    """
    # Order companies by descending market cap
    df = df.sort_values(by="market_cap_m", ascending=False)

    # Calculate each company’s market cap weight and cumulative weight
    df["weight"] = df["market_cap_m"] / df["market_cap_m"].sum()
    df["cumulative_weight"] = df["weight"].cumsum()

    # Select companies up to the 85th cumulative percentile (by market cap weight)
    portfolio = df[df["cumulative_weight"] <= cutoff].copy()

    # Allocate capital to the selected stocks, and calculate the number of shares to buy for each (using the price)
    portfolio["weight_adjusted"] = portfolio["weight"] / portfolio["weight"].sum()
    portfolio["dollars_allocated"] = portfolio["weight_adjusted"] * capital
    portfolio["num_shares"] = portfolio["dollars_allocated"] / portfolio["price"]

    return portfolio

def rebalance_portfolio(old_portfolio, new_portfolio, new_universe):
    """
    Determine which stocks to buy, sell, or keep.
    
    Args:
        old_portfolio (pd.DataFrame)
        new_portfolio (pd.DataFrame)
        new_universe (pd.DataFrame): All stocks at the second date with their prices

    
    Returns:
        pd.DataFrame: portfolio_status with actions and current values
    """

    # Merge old portfolio with full universe to get new prices for all old stocks
    status_df = old_portfolio.merge(
        new_universe[["company", "price"]],
        on="company",
        how="outer",
        suffixes=("_old", "_new")
    )

    # Merge old and new portfolios to determine buy/sell/keep decisions
    status_df = status_df.merge(
        new_portfolio[["company", "num_shares"]],
        on="company",
        how="outer",
        suffixes=("_old", "_new")
    )
    
    # Determine actions
    status_df["status"] = None

    # Stock is in the old & new portfolio -> keep
    status_df.loc[status_df["num_shares_old"].notna() & status_df["num_shares_new"].notna(), "status"] = "keep"

    # Stock was in old portfolio but not in new portfolio -> sell
    status_df.loc[status_df["num_shares_old"].notna() & status_df["num_shares_new"].isna(), "status"] = "sell"

    # Stock was not in old portfolio but in new portfolio -> buy
    status_df.loc[status_df["num_shares_old"].isna() & status_df["num_shares_new"].notna(), "status"] = "buy"
    
    # Calculate the current value of old holdings
    status_df["current_value"] = status_df["num_shares_old"].fillna(0) * status_df["price_new"].fillna(0)
    
    return status_df