# Portfolio_Optimizer
Portfolio optimization is the process of selecting an optimal portfolio (asset distribution), out of a set of considered portfolios, according to some objective. The objective typically maximizes factors such as expected return, and minimizes costs like financial risk, resulting in a multi-objective optimization problem. Factors being considered may range from tangible (such as assets, liabilities, earnings or other fundamentals) to intangible (such as selective divestment).



'''
         
This Streamlit web application is designed for portfolio optimization using Modern Portfolio Theory (MPT). Here's a detailed overview of its functionality:

### Features:

1. **File Upload**:
   - Allows users to upload a CSV file containing asset prices.
   - The file should have a date column (`time`) in `MM-DD-YYYY` format and asset price columns in numerical format.

2. **Data Processing**:
   - Reads the uploaded CSV file, converts the `time` column to datetime format, and sets it as the DataFrame index.
   - Drops the original `time` column from the DataFrame.

3. **Modern Portfolio Theory Visualization**:
   - Defines a function to plot efficient frontier and random portfolios with optimal portfolio highlighting.

4. **User Inputs**:
   - Allows users to select the optimization method (`Sharpe` or `Min Volatility`) and the range of weights for the assets.
   - Provides sliders for users to set the weight range.

5. **Optimization**:
   - Calculates expected returns and sample covariance matrix from the uploaded data.
   - Uses the selected optimization method to compute optimal weights:
     - **Sharpe Ratio Optimization**: Maximizes the Sharpe ratio.
     - **Min Volatility Optimization**: Minimizes portfolio volatility.
   - Displays the optimal weights as a bar chart and DataFrame.
   - Plots the efficient frontier and random portfolios.

6. **Portfolio Performance**:
   - Multiplies `Annual return` and `Annual Volatility` values by 100 for better readability.
   - Displays the portfolio performance metrics in a Table.

### Usage:

1. **Upload CSV File**:
   - Upload a CSV file with the specified format.

### Example CSV Format:

Ensure your CSV file matches the following format to avoid errors:
```
time, Asset1, Asset2, Asset3, ...
01-01-2020, 100.0, 200.0, 150.0, ...
01-02-2020, 101.0, 201.0, 151.0, ...
...
```

2. **Set Optimization Parameters**:
   - Select the optimization method (`Sharpe` or `Min Volatility`).
   - Adjust the weight range using the slider.

3. **Run Optimization**:
   - Click the "Run optimization" button to compute and display the optimal portfolio weights and performance.


         
By following these steps, users can efficiently optimize their portfolios and visualize the results using this Streamlit application.


Created by @VanHe1sing  
         
TradingView:https://www.tradingview.com/u/VanHe1sing/#published-scripts     
Telegram:https://t.me/IvanKocherzhat\n
X:https://x.com/sxJEoRg7wwLR6ug

'''