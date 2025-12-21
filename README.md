# Pairs-Trading-Cointegrated-Asset-Detection
Python application that identifies cointegrated asset pairs suitable for pairs trading using Yahoo Finance data. The application is implemented without using statsmodels library.

# How it works:

The program uses data downloaded from Yahoo Finance via the yfinance library. It takes a CSV file containing ticker symbols as input and downloads historical price data over a specified time range (by default, from one year ago to today, with daily frequency).

Since the downloaded data may contain missing values, the program counts the number of NaNs for each ticker and prints this information in a tabular form. If any ticker has more than 5% missing data (i.e. the number of NaNs exceeds 5% of the total number of data points), this is explicitly reported. Any pair containing such an asset is also correctly flagged. Missing values are filled using linear interpolation.

In the first filtering step, only asset pairs with a Pearson correlation coefficient greater than a given threshold (default: 0.8) are considered. Next, one asset is linearly regressed on the other, yielding the hedge ratio and the spread.

The program then performs an Augmented Dickey–Fuller (ADF) test on the spread, including a constant term but no trend. To select the appropriate lag order, the ADF test is performed for lag orders from 1 up to a maximum value (default: 4), and the specification that minimizes the Akaike Information Criterion (AIC) is chosen.

The critical value for the ADF test is computed using the finite-sample approximation

$`ADF_{crit} = -2.86 - \frac{2.89}{N} - \frac{4.234}{N^2} - \frac{40.04}{N^3}`$

Where N is time series length. The numerical correspond to significance level of $`\alpha = 5\%`$. 

All identified cointegrated pairs are saved to CSV file.

# How to use:

Clone the repository and install the required dependencies:





