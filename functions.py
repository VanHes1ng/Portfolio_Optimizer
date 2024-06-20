import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


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

    def plot_ef(n_samples, ef, label):
        w               = np.random.dirichlet(np.ones(ef.n_assets), n_samples)
        rets            = w.dot(ef.expected_returns)
        stds            = np.sqrt(np.diag(w @ ef.cov_matrix @ w.T))
        sharpes         = rets / stds
        plt.style.use("_classic_test_patch")
        fig, ax         = plt.subplots(figsize=(15,7))
        ax.scatter(stds, rets, marker=".", c=sharpes, cmap="winter")

        # Portfolio
        ret_tangent, std_tangent, _ = ef.portfolio_performance()


        #Plot of portfolios
        ax.plot(std_tangent, ret_tangent, marker='*', color='r', markersize=12, label=label)

        # Output
        ax.set_title("Random Portfolios with Optimal Portfolio")
        ax.legend()

        st.subheader("The Modern Portfolio Theory (MPT)", help = "The Modern Portfolio Theory (MPT) refers to an investment theory that allows investors to assemble an asset portfolio that maximizes expected return for a given level of risk. The theory assumes that investors are risk-averse; for a given level of expected return, investors will always prefer the less risky portfolio.")
        st.pyplot(fig)