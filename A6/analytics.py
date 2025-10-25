def VolatilityDecorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        # Handle nested decorators (dict chaining)
        if isinstance(result, dict):
            data = result.get("returns")
            if data is None:
                return result
        else:
            data = result

        if not data:
            vol = 0.0
        else:
            mean = sum(data) / len(data)
            variance = sum((x - mean) ** 2 for x in data) / len(data)
            vol = variance ** 0.5

        # When stacked, merge results
        if isinstance(result, dict):
            result["volatility"] = vol
            return result
        else:
            return {"returns": data, "volatility": vol}
    return wrapper


def BetaDecorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        market_returns = kwargs.get("market_returns", [])

        # Handle nested results
        if isinstance(result, dict):
            data = result.get("returns")
            if data is None:
                return result
        else:
            data = result

        if not data or not market_returns or len(data) != len(market_returns):
            beta = 0.0
        else:
            asset_mean = sum(data) / len(data)
            market_mean = sum(market_returns) / len(market_returns)
            covariance = sum(
                (data[i] - asset_mean) * (market_returns[i] - market_mean)
                for i in range(len(data))
            ) / len(data)
            market_var = sum((x - market_mean) ** 2 for x in market_returns) / len(market_returns)
            beta = covariance / market_var if market_var != 0 else 0.0

        if isinstance(result, dict):
            result["beta"] = beta
            return result
        else:
            return {"returns": data, "beta": beta}
    return wrapper


def DrawdownDecorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        if isinstance(result, dict):
            data = result.get("returns")
            if data is None:
                return result
        else:
            data = result

        if not data:
            dd = 0.0
        else:
            if all(-1 < x < 1 for x in data):
                cumulative = [1]
                for r in data:
                    cumulative.append(cumulative[-1] * (1 + r))
                cumulative = cumulative[1:]
            else:
                cumulative = data

            peak = cumulative[0]
            max_dd = 0.0
            for v in cumulative:
                peak = max(peak, v)
                dd = (peak - v) / peak if peak != 0 else 0
                max_dd = max(max_dd, dd)
            dd = max_dd

        if isinstance(result, dict):
            result["max_drawdown"] = dd
            return result
        else:
            return {"returns": data, "max_drawdown": dd}
    return wrapper


if __name__ == "__main__":
    def sample_returns():
        return [0.05, -0.02, 0.03, 0.01, -0.01, 0.04, -0.03]

    decorated = DrawdownDecorator(BetaDecorator(VolatilityDecorator(sample_returns)))
    print(decorated())
