# Imports
import streamlit as st
import pandas as pd
import numpy as np
import time
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns, HRPOpt


from streamlit.components.v1 import html

from functions import portfolio_optimization as po

# ------------------------------------------------------------------------------------------------------------------------------------
#Set Page Configurations
# ------------------------------------------------------------------------------------------------------------------------------------

st.set_page_config(
                    page_title = "Portfolio Optimization",
                    page_icon  = "📊",
                    layout     = "wide"
                                )

# ------------------------------------------------------------------------------------------------------------------------------------
# Upload a file
# ------------------------------------------------------------------------------------------------------------------------------------
c1_,c2_,c3_= st.columns([1,1,1])

c_1,c_2,c_3= st.columns([1,6,1])


c2_.title("**Portfolio :blue[Optimization]**")

with st.sidebar:
    st.title("**Portfolio :blue[Optimization]**")

uploaded_file = c_2.file_uploader(":blue[Upload your .csv file with assets prices]")
c_2.write("---")
c_2.info('''**Ensure your .csv file matches the provided example to avoid errors.**\n 
            ⚠️FORMAT: [time column: MM-DD-YYYY, Asset name columns: 0.000]''', icon="📝")

c_2.write("***Example .csv***")
c_2.image("images/image.png")


if uploaded_file is not None:
    progress_text = "Operation in progress. Please wait."
    my_bar = c_2.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.empty()

    up_done = c_2.success('Uploaded', icon="✅")
    time.sleep(1.0)
    up_done.empty()

    df = pd.DataFrame()
    df = pd.read_csv(uploaded_file)
    # Setting Date as index
    df['time'] = pd.to_datetime(df['time'], format='%m-%d-%Y')
    df = df.set_index(df['time'].values)

    # Removing the Date Column
    df.drop(columns=['time'], axis=1, inplace=True)

if uploaded_file is None:
    c_2.warning('Please upload a file.')
    st.stop()

    # PLOT
    c_2.subheader("The Modern Portfolio Theory (MPT)", 
                  help = '''The Modern Portfolio Theory (MPT) refers to an investment theory
                    that allows investors to assemble an asset portfolio that maximizes expected return for a given level of risk. 
                    The theory assumes that investors are risk-averse; for a given level of expected return, investors will always prefer the less risky portfolio.''')
    c_2.pyplot(fig)

# ------------------------------------------------------------------------------------------------------------------------------------
# INPUTS
# ------------------------------------------------------------------------------------------------------------------------------------

c_2.write("###")
c_2.write("---")
c_2.write("###")

if uploaded_file is not None:
    c_2.subheader("Method of Optimization")
    method = c_2.radio(
                      "Set a method and Run optimization ⚙️",
                      key        =    "visibility",
                      options    =   ["Sharpe", "Min Volatility"],
                      horizontal =   True
                        )
    
    values = c_2.slider(
                        "Select a range of weights %",
                        0.0, 1.0, (0.05, 0.65)
                        )
    
    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(df)
    S  = risk_models.sample_cov(df)

    # Optimize for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S, weight_bounds=values)

    button = c_2.button("Run optimization")
    if not button:
        st.stop()

    if method == "Sharpe" and button:
        c_2.write("---")
        c_2.subheader(f"Optimal :blue[{method}] Weights")
        c_2.write("###")
        weights = ef.max_sharpe()

        cleaned_weights = ef.clean_weights()

        c_2.bar_chart(cleaned_weights, use_container_width=True, height=500)
        c_2.dataframe(cleaned_weights, use_container_width = True)
        c_2.write("---")



    if method == "Min Volatility" and button:
        c_2.write("---")
        c_2.subheader(f"Optimal :blue[{method}] Weights")
        c_2.write("###")
        weights = ef.min_volatility()
  
        cleaned_weights = ef.clean_weights()

        c_2.bar_chart(cleaned_weights, use_container_width=True, height=500)
        c_2.dataframe(cleaned_weights, use_container_width = True)
        c_2.write("---")

    with c_2:
        po.plot_ef(5000, ef, method)


    weights = pd.DataFrame({'Weights': weights})

# ------------------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------------------------------
# Portfolio Performance
# ------------------------------------------------------------------------------------------------------------------------------------

    c_2.write("---")
    c_2.subheader("Portfolio :blue[Performance]")

    asset_names = df.columns

    for asset in df.columns:
        df[asset] = df[asset] * weights.loc[asset, 'Weights']

    df['Portfolio'] = df.sum(axis=1)

    final_df = df[['Portfolio']]

    maxdd_      = np.round(po.max_drawdown(final_df['Portfolio'])*100, 2)
    maxdd_rol   = po.rol_max_drawdown(final_df['Portfolio']*100)
    cum_ret     = np.round((np.exp(np.log1p(final_df.pct_change()['Portfolio']).cumsum()).iloc[-1]) * 100, 2)

    dail_vol    = np.round(po.daily_vol(final_df).iloc[0]*100, 2)
    monthly_vol = np.round(po.daily_vol(final_df).iloc[0]*100 * np.sqrt(30), 2)
    anuall_vol  = np.round(po.daily_vol(final_df).iloc[0]*100 * np.sqrt(365), 2)

    sharpe      = np.round(po.sharpe(final_df).iloc[0], 2)
    sortino     = np.round(po.sortino(final_df).iloc[0], 2)
    omega       = np.round(po.omega(final_df).iloc[0], 2)


    # Portfolio Metrics Plot
    with c_2:
        st.area_chart(final_df/10)
        st.write("---")

        c1,c2,c3= st.columns([2,3,1])
        c1.write(f"Cumulative returns:"),        c2.write(f"{cum_ret} %")
        c1.write("---"),                         c2.write("---")
        c1.write(f"Sharpe Ratio:"),              c2.write(f"{sharpe}")
        c1.write(f"Sortino Ratio:"),             c2.write(f"{sortino}")
        c1.write(f"Omega Ratio:"),               c2.write(f"{omega}")
        c1.write("---"),                         c2.write("---")
        c1.write(f"AVG Daily Volatility:"),      c2.write(f"{dail_vol} %")
        c1.write(f"AVG Monthly Volatility:"),    c2.write(f"{monthly_vol} %")
        c1.write(f"AVG Anuall Volatility:"),     c2.write(f"{anuall_vol} %")
        c1.write("---"),                         c2.write("---")    
        c1.write(f"Max Draw Down:"),             c2.write(f"{maxdd_} %")


        st.area_chart(maxdd_rol*100, color="#d14747")
    
else:
    st.stop()