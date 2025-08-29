import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import pandas as pd
from src import helpers



@pytest.fixture
def first_date_data():
    return pd.DataFrame({
        "date": ["8/04/2025"] * 4,
        "company": ["A", "B", "C", "D"],
        "market_cap_m": [1000, 900, 800, 700],
        "price": [10, 20, 5, 7]
    })

@pytest.fixture
def second_date_data():
    return pd.DataFrame({
        "date": ["9/05/2025"] * 4,
        "company": ["A", "B", "C", "E"],
        "market_cap_m": [1100, 850, 750, 600],
        "price": [11, 21, 6, 8]
    })

def test_build_index(first_date_data):
    portfolio = helpers.build_index(first_date_data, capital=100, cutoff=0.85)
    # Check weights sum to 1 after adjustment
    assert portfolio["weight_adjusted"].sum() == 1
    # Check shares are positive
    assert (portfolio["num_shares"] > 0).all()

def test_rebalance_portfolio(first_date_data, second_date_data):
    old_portfolio = helpers.build_index(first_date_data, capital=100, cutoff=0.85)
    new_portfolio = helpers.build_index(second_date_data, capital=100, cutoff=0.85)
    status_df = helpers.rebalance_portfolio(old_portfolio, new_portfolio, second_date_data)

    assert all(status in ("keep", "sell", "buy", None) for status in status_df["status"])

    # Current values non-negative
    assert (status_df["current_value"] >= 0).all()

    # All companies accounted for
    expected_companies = set(old_portfolio["company"]).union(new_portfolio["company"]).union(second_date_data["company"])
    assert set(status_df["company"]) == expected_companies
