import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from pypfopt import expected_returns
from scipy.optimize import minimize


class portfolio_optimization:
    def sharpe(src): 
        d_r     = src.pct_change()
        std     = d_r.std()
        mean    = d_r.mean()
        return (mean / std) * np.sqrt(365)


    def sortino(src):
        d_r      = src.pct_change()
        stdv_neg = (d_r[d_r < 0]*-1).std()
        mean     = d_r.mean()
        return (mean / stdv_neg) * np.sqrt(365)

    def omega(src):
        d_r      = src.pct_change()
        stdv_neg = (d_r[d_r < 0]*-1).sum()
        stdv_pos = (d_r[d_r > 0]).sum()
        return (stdv_pos / stdv_neg) 


    def max_drawdown(src):
        return_series = src.pct_change()
        comp_ret      = (return_series+1).cumprod()
        peak          = comp_ret.expanding(min_periods=1).max()
        dd            = (comp_ret/peak)-1
        return dd.min()
    
    def rol_max_drawdown(src):
        return_series = src.pct_change()
        comp_ret      = (return_series+1).cumprod()
        peak          = comp_ret.expanding(min_periods=1).max()
        dd            = (comp_ret/peak)-1
        return dd

    def daily_vol(src):
        d_r = src.pct_change()
        return d_r.std()

    @staticmethod
    def plot_ef(n_samples, ef, label, custom_weights=None):
        w = np.random.dirichlet(np.ones(ef.n_assets), n_samples)
        rets = w.dot(ef.expected_returns)
        stds = np.sqrt(np.diag(w @ ef.cov_matrix @ w.T))
        sharpes = rets / stds
        plt.style.use("_classic_test_patch")
        fig, ax = plt.subplots(figsize=(15,7))
        ax.scatter(stds, rets, marker=".", c=sharpes, cmap="winter")

        # Portfolio performance calculation
        if custom_weights is not None:
            # For custom optimization methods (like Omega)
            portfolio_ret = ef.expected_returns.dot(custom_weights)
            portfolio_std = np.sqrt(custom_weights.T @ ef.cov_matrix @ custom_weights)
            ret_tangent, std_tangent = portfolio_ret, portfolio_std
        else:
            # For EfficientFrontier optimization methods
            ret_tangent, std_tangent, _ = ef.portfolio_performance()

        # Plot of portfolios
        ax.plot(std_tangent, ret_tangent, marker='*', color='r', markersize=12, label=label)

        # Output
        ax.set_title("Random Portfolios with Optimal Portfolio")
        ax.legend()

        st.subheader("The Modern Portfolio Theory (MPT)", help="The Modern Portfolio Theory (MPT) refers to an investment theory that allows investors to assemble an asset portfolio that maximizes expected return for a given level of risk. The theory assumes that investors are risk-averse; for a given level of expected return, investors will always prefer the less risky portfolio.")
        st.pyplot(fig)

    @staticmethod
    def omega_ratio(weights, returns, threshold=0):
        """
        Calculate the Omega ratio for a portfolio
        
        Parameters:
        weights (array): Portfolio weights
        returns (DataFrame): Asset returns
        threshold (float): Minimum acceptable return
        
        Returns:
        float: Negative Omega ratio (negative for minimization)
        """
        portfolio_returns = np.sum(returns * weights, axis=1)
        
        # Separate returns above and below threshold
        excess_returns = portfolio_returns - threshold
        positive_excess = np.maximum(excess_returns, 0)
        negative_excess = np.maximum(-excess_returns, 0)
        
        # Calculate expected values
        expected_positive = np.mean(positive_excess)
        expected_negative = np.mean(negative_excess)
        
        # Avoid division by zero
        if expected_negative == 0:
            return -1000  # Large negative number for optimization
        
        # Return negative omega ratio (since we're minimizing)
        return -(expected_positive / expected_negative)

    @staticmethod
    def optimize_omega(returns, threshold=0.0, bounds=(0.0, 1.0)):
        """
        Find the portfolio weights that maximize the Omega ratio
        
        Parameters:
        returns (DataFrame): Asset returns
        threshold (float): Minimum acceptable return
        bounds (tuple): (min_weight, max_weight) for each asset
        
        Returns:
        array: Optimal weights
        """
        n_assets = returns.shape[1]
        
        # Initial weights (equal weight)
        init_weights = np.array([1/n_assets] * n_assets)
        
        # Constraints
        bounds = [bounds for _ in range(n_assets)]
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # weights sum to 1
        ]
        
        # Optimize
        result = minimize(
            portfolio_optimization.omega_ratio,  # Now using class method directly
            init_weights,
            args=(returns, threshold),
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return result.x 