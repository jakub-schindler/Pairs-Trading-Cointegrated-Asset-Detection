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

## Installation using virtualenv (recommended)

git clone https://github.com/jakub-schindler/Pairs-Trading-Cointegrated-Asset-Detection.git \
cd Pairs-Trading-Cointegrated-Asset-Detection 

python -m venv .venv \
source .venv/bin/activate  # Linux / macOS \
.venv\Scripts\activate     # Windows

pip install -e .

## Basic usage:

Prepare an input CSV file. It should be a single column named "tickers" with a ticker name in each row. You can use an example file "tickers_example.csv". 

The simplest way to run it is:

find-pairs --input path_to_tickers.csv --output outcome_file.csv

This will:

-download historical price data from Yahoo Finance, \
-linearly interpolate missing values, \
-flag assets with more than 5% missing data, \
-filter asset pairs by Pearson correlation, \
-estimate hedge ratios using OLS regression, \
-perform an Augmented Dickey-Fuller test on the spread, \
-save all detected cointegrated pairs to the output CSV file. (if not existing, then it will be created automatically)

## Examples:

You can use the example_tickers.csv file:

find-pairs --input example_tickers.csv --output outcome_file.csv

This will create a file named outcome_file.csv or append if it already exists.

Full usage:

find-pairs --input example_tickers.csv --output outcome_file.csv --corr_threshold 0.5 --start_date 2022-10-05 --end_date 2024-05-22 --interval 5d

## Command line arguments:

| Argument  | Description | Default | 
| ------------- | ------------- | ------------- |
| --input | Path to the input csv file | required |
| --output | Path to the output csv file. If the file doesn't exist it will be created automatically | required |
| --corr_threshold | Minimum Pearson correlation coefficient threshold  | 0.8 |
| --start_date | Start date (YYYY-MM-DD) | one year before end_date |
| --end_date | End date (YYYY-MM-DD) | today |
| --interval | Time interval between data points. Available values: {1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo} | 1d |

To check available options use:
find-pairs --help






