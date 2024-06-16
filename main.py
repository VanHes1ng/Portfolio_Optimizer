# Imports
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import copy
import time
import quantstats as qs

from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns, HRPOpt
from PIL import Image
from streamlit.components.v1 import html

# ------------------------------------------------------------------------------------------------------------------------------------
#Set Page Configurations
# ------------------------------------------------------------------------------------------------------------------------------------

st.set_page_config(
                    page_title = "Portfolio Optimization",
                    page_icon  = "^",
                    layout     = "wide"
                                )

# ------------------------------------------------------------------------------------------------------------------------------------
# Upload a file
# ------------------------------------------------------------------------------------------------------------------------------------

st.title("**Portfolio :blue[Optimization]**")


c1,c2= st.columns([1,2])
uploaded_file = c1.file_uploader(":blue[Upload your .csv file with assets prices]")
c1.write("---")
c1.info('Ensure your .csv file matches the provided example to avoid errors', icon="📝")

c2.write("***Example .csv***")

c2.image("images/CSV_FORMAT.png")
c2.write('Upload your file in the next format: [time column: MM-DD-YYYY, Asset name columns: 0.000] and the Optimizer will perform process of optimization automatically.')

col1,col2= st.columns([1,2])

if uploaded_file is not None:
    progress_text = "Operation in progress. Please wait."
    my_bar = col2.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.empty()

    up_done = col2.success('Uploaded', icon="✅")
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
    col2.warning('Please upload a file.')
    st.stop()