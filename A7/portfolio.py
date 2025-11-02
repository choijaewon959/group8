import pandas as pd
import numpy as np
import json
from data_loader import load_data_pandas
from metrics import rolling_metrics_pandas
# for parallel programing library
from concurrent.futures import ProcessPoolExecutor, as_completed
# for measuring performance libraries
from patterns.builder_pattern import PortfolioBuilder, Portfolio

def long_only_MA20_port_construction_with_time_series(mkt_df, symbol, builder: PortfolioBuilder):

    df = rolling_metrics_pandas(mkt_df, symbol, ['price'], window=20)   
    df['position'] = 0
    df.loc[df['price'] < df['price_MA_20'], 'position'] = 1
    df['cumulative_position'] = df['position'].cumsum()
    df['portfolio_value'] = df['cumulative_position'] * df['price']

    # final position
    final_qty = df['cumulative_position'].iloc[-1]
    final_price = df['price'].iloc[-1]
    
    # filter valid transaction time series
    df = df[df['position'] > 0]

    # use builder
    builder.add_position(symbol, final_qty, final_price, df)

    return df, builder


def compute_position_metrics(symbol: str, df_ts: pd.DataFrame) -> dict:
    
    latest_value = float(df_ts["portfolio_value"].iloc[-1])
    df_ts["returns"] = df_ts["portfolio_value"].pct_change().fillna(0)
    volatility = float(df_ts["returns"].std())
    drawdown = float((df_ts["portfolio_value"] / df_ts["portfolio_value"].cummax() - 1).min())
    
    return {"symbol": symbol, "value": latest_value, "volatility": volatility, "drawdown": drawdown}


def compute_portfolio_metrics(portfolio: Portfolio) -> dict:

    port_result = {"name": getattr(portfolio, "port_name", None)}

    # in case of main portfolio - contain 'owner'
    if hasattr(portfolio, "owner") and portfolio.owner is not None:
        port_result["owner"] = portfolio.owner

    positions_metrics = []
    futures = {}
    with ProcessPoolExecutor() as executor:
        for pos in getattr(portfolio, "positions", []):
            fut = executor.submit(compute_position_metrics, pos["symbol"], pos["ts"])
            futures[fut] = pos
        for fut in as_completed(futures):
            positions_metrics.append(fut.result())
    
    if positions_metrics:
        port_result["positions"] = positions_metrics

    sub_metrics_list = []
    for sub in getattr(portfolio, "sub_portfolios", []):
        sub_metrics = compute_portfolio_metrics(sub)
        if sub_metrics.get("positions") or sub_metrics.get("sub_portfolios"):
            sub_metrics_list.append(sub_metrics)
    if sub_metrics_list:
        port_result["sub_portfolios"] = sub_metrics_list

    # Aggregate
    all_values = [p["value"] for p in positions_metrics]
    sub_values = [sub.get("total_value", 0) for sub in sub_metrics_list]
    total_value = sum(all_values) + sum(sub_values)
    port_result["total_value"] = total_value

    if all_values:
        total_weight = sum(all_values) if sum(all_values) > 0 else 1
        port_result["aggregate_volatility"] = sum(
            v * val / total_weight for v, val in zip([p["volatility"] for p in positions_metrics], all_values)
        )
    else:
        port_result["aggregate_volatility"] = 0

    max_dd = min(
        [p["drawdown"] for p in positions_metrics] +
        [sub.get("max_drawdown", 0) for sub in sub_metrics_list] +
        [0]
    )
    port_result["max_drawdown"] = max_dd

    return port_result



def compute_portfolio_metrics_sequential(portfolio: Portfolio) -> dict:

    port_result = {"name": getattr(portfolio, "port_name", None)}

    # in case of main portfolio - contain 'owner'
    if hasattr(portfolio, "owner") and portfolio.owner is not None:
        port_result["owner"] = portfolio.owner

    positions_metrics = []
    for pos in getattr(portfolio, "positions", []):
        metrics = compute_position_metrics(pos["symbol"], pos["ts"])
        positions_metrics.append(metrics)
    if positions_metrics:
        port_result["positions"] = positions_metrics

    sub_metrics_list = []
    for sub in getattr(portfolio, "sub_portfolios", []):
        sub_metrics = compute_portfolio_metrics_sequential(sub)
        if sub_metrics.get("positions") or sub_metrics.get("sub_portfolios"):
            sub_metrics_list.append(sub_metrics)
    if sub_metrics_list:
        port_result["sub_portfolios"] = sub_metrics_list

    # Aggregate calculation
    all_values = [p["value"] for p in positions_metrics]
    sub_values = [sub.get("total_value", 0) for sub in sub_metrics_list]
    total_value = sum(all_values) + sum(sub_values)
    port_result["total_value"] = total_value

    # weighted volatility
    if all_values:
        total_weight = sum(all_values) if sum(all_values) > 0 else 1
        port_result["aggregate_volatility"] = sum(
            v * val / total_weight for v, val in zip([p["volatility"] for p in positions_metrics], all_values)
        )
    else:
        port_result["aggregate_volatility"] = 0

    # worst drawdown
    max_dd = min(
        [p["drawdown"] for p in positions_metrics] +
        [sub.get("max_drawdown", 0) for sub in sub_metrics_list] +
        [0]
    )
    port_result["max_drawdown"] = max_dd

    return port_result

# -----------------------------
# Execution example
# -----------------------------
if __name__ == "__main__":
    # load whole market data
    df_prices, _, _ = load_data_pandas("./data/market_data-1.csv")

    # build portfolio object
    main_builder = PortfolioBuilder("Main Portfolio", "wanann")
    sub_builder = PortfolioBuilder("SPY Portfolio", "wanann")

    # Implement a function that computes metrics for a single position
    main_ts, main_builder = long_only_MA20_port_construction_with_time_series(df_prices, "AAPL", main_builder)
    sub_ts, sub_builder = long_only_MA20_port_construction_with_time_series(df_prices, "SPY", sub_builder)
    # Add to Subportfolio to fit with output sample
    main_builder.add_subportfolio(sub_builder.portfolio)

    # Use multiprocessing to compute metrics for all positions in parallel.
    final_metrics = compute_portfolio_metrics(main_builder.portfolio)
    # Implement a sequential version for comparison.
    metrics_sequential = compute_portfolio_metrics_sequential(main_builder.portfolio)
    
    print("MultiProcessing Metrics:\n", json.dumps(final_metrics, indent=2))
    print("Sequential Metrics:\n", json.dumps(metrics_sequential, indent=2))

    

