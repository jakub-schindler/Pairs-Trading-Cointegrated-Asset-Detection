# Pairs-Trading-Cointegrated-Asset-Detection
Python application that identifies cointegrated asset pairs suitable for pairs trading using Yahoo Finance data. The application was written without using statsmodels library.

How it works:

The program uses data downloaded from Yahoo Finance by using yfinance library. It takes a CSV file of tickers as input and download the data in a given time range (by default from 1y ago to today in icrements of 1 day). Since the data tends to have some missing values, the program count how many NaNs there are for each ticker and print this info in a form of a table. If any on the tickers has more than 5% of their data missing (it's number of NaNs > 5% * total amount of data points), this info is printed out. Any pair containing this asset will also be correctly flagged. The missing data is linearly interpolated. 

At first the pairs are fitlered, by only passing those that have a correlation coefficient larger than a certain threshold (by default the threshold is 0.8). Next one of the assets is regressed on the other one, giving us a hedge ratio and spread. 

The program performs and Augmented-Dickey-Fueller test with a constant and no trend on the spread. It's my own implementation of ADF. The critical value of ADF is caluclated as such:
$`ADF_{crit} = -2.86 - 2.89/N - 4.234 / N**2 - 40.04 / N**3`$
