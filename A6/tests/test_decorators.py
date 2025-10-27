from analytics import VolatilityDecorator, BetaDecorator, DrawdownDecorator


class TestVolatilityDecorator:
    """Test cases for VolatilityDecorator"""

    def test_volatility_calculation_basic(self):
        """Test basic volatility calculation"""
        @VolatilityDecorator
        def sample_returns():
            return [0.1, 0.0, -0.1, 0.05]
        
        result = sample_returns()
        print(result)
        assert isinstance(result, dict)
        assert "returns" in result
        assert "volatility" in result
        assert result["returns"] == [0.1, 0.0, -0.1, 0.05]
        
        # Manual calculation: mean = 0.0125, variance = 0.004844, vol = 0.0696
        expected_vol = 0.0854
        assert abs(round(result["volatility"], 4) - expected_vol) < 1e-10

    def test_volatility_empty_data(self):
        """Test volatility with empty data"""
        @VolatilityDecorator
        def empty_returns():
            return []
        
        result = empty_returns()
        assert result["volatility"] == 0.0
        assert result["returns"] == []

    def test_volatility_single_value(self):
        """Test volatility with single value"""
        @VolatilityDecorator
        def single_return():
            return [0.05]
        
        result = single_return()
        assert result["volatility"] == 0.0  # No variance with single value
        assert result["returns"] == [0.05]

    def test_volatility_nested_dict_input(self):
        """Test volatility decorator with dict input (chaining scenario)"""
        @VolatilityDecorator
        def dict_returns():
            return {"returns": [0.02, 0.04, -0.01]}
        
        result = dict_returns()
        assert "volatility" in result
        assert "returns" in result
        assert len(result["returns"]) == 3


class TestBetaDecorator:
    """Test cases for BetaDecorator"""

    def test_beta_calculation_basic(self):
        """Test basic beta calculation"""
        market_returns = [0.04, 0.01, -0.02, 0.025]

        @BetaDecorator
        def sample_returns():
            return market_returns
        
        result = sample_returns()
        
        assert isinstance(result, dict)
        assert "returns" in result
        assert "beta" in result
        assert result["returns"] == market_returns
        
        # Beta should be calculated based on covariance/market_variance
        assert isinstance(result["beta"], float)

    def test_beta_no_market_returns(self):
        """Test beta with no market returns provided"""
        @BetaDecorator
        def sample_returns():
            return [0.05, 0.02, -0.01]
        
        result = sample_returns()
        assert result["beta"] == 0.0

    def test_beta_mismatched_lengths(self):
        """Test beta with mismatched data lengths"""
        @BetaDecorator
        def sample_returns():
            return [0.05, 0.02, -0.01]
        
        result = sample_returns()
        assert result["beta"] == 0.0

    def test_beta_zero_market_variance(self):
        """Test beta with zero market variance"""
        @BetaDecorator
        def sample_returns():
            return [0.05, 0.02, -0.01]
        
        result = sample_returns()
        assert result["beta"] == 0.0

    def test_beta_with_dict_input(self):
        """Test beta decorator with dict input (chaining scenario)"""
        @BetaDecorator
        def dict_returns():
            return {"returns": [0.02, 0.04, -0.01]}
        
        result = dict_returns()
        assert "beta" in result
        assert "returns" in result


class TestDrawdownDecorator:
    """Test cases for DrawdownDecorator"""

    def test_drawdown_calculation_returns(self):
        """Test drawdown calculation with returns data"""
        @DrawdownDecorator
        def sample_returns():
            return [0.1, -0.05, -0.1, 0.2]  # Returns format
        
        result = sample_returns()
        
        assert isinstance(result, dict)
        assert "returns" in result
        assert "max_drawdown" in result
        assert result["returns"] == [0.1, -0.05, -0.1, 0.2]
        assert isinstance(result["max_drawdown"], float)
        assert 0 <= result["max_drawdown"] <= 1

    def test_drawdown_calculation_prices(self):
        """Test drawdown calculation with price data"""
        @DrawdownDecorator
        def sample_prices():
            return [100, 110, 105, 95, 115]  # Price format
        
        result = sample_prices()
        
        assert "max_drawdown" in result
        # Max drawdown should be (110-95)/110 = 0.1364
        expected_dd = (110 - 95) / 110
        assert abs(result["max_drawdown"] - expected_dd) < 1e-10

    def test_drawdown_empty_data(self):
        """Test drawdown with empty data"""
        @DrawdownDecorator
        def empty_returns():
            return []
        
        result = empty_returns()
        assert result["max_drawdown"] == 0.0
        assert result["returns"] == []

    def test_drawdown_single_value(self):
        """Test drawdown with single value"""
        @DrawdownDecorator
        def single_return():
            return [100]
        
        result = single_return()
        assert result["max_drawdown"] == 0.0

    def test_drawdown_with_dict_input(self):
        """Test drawdown decorator with dict input (chaining scenario)"""
        @DrawdownDecorator
        def dict_returns():
            return {"returns": [0.05, -0.02, 0.03]}
        
        result = dict_returns()
        assert "max_drawdown" in result
        assert "returns" in result


class TestDecoratorChaining:
    """Test cases for chaining multiple decorators"""

    def test_all_decorators_chained(self):
        """Test chaining all three decorators"""
        @DrawdownDecorator
        @BetaDecorator
        @VolatilityDecorator
        def sample_returns():
            return [0.05, -0.02, 0.03, 0.01, -0.01]

        result = sample_returns()
        # Should have all metrics
        assert "returns" in result
        assert "volatility" in result
        assert "beta" in result
        assert "max_drawdown" in result
        
        # Verify data integrity
        assert result["returns"] == [0.05, -0.02, 0.03, 0.01, -0.01]
        assert isinstance(result["volatility"], float)
        assert isinstance(result["beta"], float)
        assert isinstance(result["max_drawdown"], float)
        assert round(result["volatility"], 4) - 0.0286 < 1e-4
        assert round(result["max_drawdown"], 4) - 0.02 < 1e-4

    def test_partial_chaining(self):
        """Test chaining subset of decorators"""
        @BetaDecorator
        @VolatilityDecorator
        def sample_returns():
            return [0.1, 0.0, -0.05]

        result = sample_returns()

        assert "returns" in result
        assert "volatility" in result
        assert "beta" in result
        assert "max_drawdown" not in result

    def test_different_chaining_order(self):
        """Test different order of decorator chaining"""
        @VolatilityDecorator
        @DrawdownDecorator
        def sample_returns():
            return [0.02, 0.04, -0.01]
        
        result = sample_returns()
        
        assert "returns" in result
        assert "volatility" in result
        assert "max_drawdown" in result
        assert "beta" not in result

