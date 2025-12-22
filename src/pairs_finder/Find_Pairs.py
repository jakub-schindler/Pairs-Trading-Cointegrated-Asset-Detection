from datetime import date, timedelta
import pandas as pd
import yfinance as yf
import numpy as np
from .ADF import ADF, ADF_crit_values
from typing import Optional


'''
The role of this python program is to find suitable pairs of financial instruments that can be used to execute
pair trading strategies. First it takes a pool of tickers, download their closing prices from Yahoo Finance and going 
pair by pair, calclates their correlation coefficients. If this coefficient is larger that some critical value,
hedge ratio is caluclated and an Augmented-Dickey-Fueller test is performed. Pairs that pass it are returned.
'''

def find_pairs(tickers, critical_corrcoef = 0.8, start_date: Optional[date] = None, end_date: Optional[date] = None, interval='1d', max_ADF_order = 4):
	if end_date is None:
		end_date = date.today()
	if start_date is None:
		start_date = end_date - timedelta(days = 365)

	#download data from a list of ticker
	data = yf.download(tickers, start = start_date, end = end_date, interval = interval, auto_adjust = True)

	#Print the information about the number of missing values in every asset

	NaN_key_names = np.concatenate((['Expected number of data points', 'total NaNs'], [t + ' Nans' for t in tickers]))
	Nan_values = [data[('Close', t)].isna().sum() for t in tickers]
	Total_Nans = np.sum(Nan_values)
	NaN_values_with_total = np.concatenate(([len(data.index.get_level_values(0)), Total_Nans], Nan_values))

	df_NaN = pd.DataFrame(NaN_values_with_total, index = NaN_key_names, columns = ['Values'])
	print(df_NaN)

	flagged_tickers = df_NaN.drop('total NaNs')
	flagged_tickers = flagged_tickers.drop('Expected number of data points')
	flagged_tickers = flagged_tickers[flagged_tickers['Values'] > df_NaN.loc['Expected number of data points', 'Values']*0.05]

	if len(flagged_tickers.index) != 0:
		flagged_tickers = [t.split(" ")[0] for t in flagged_tickers.index.to_numpy()]
		print('\nWARNING: The following tickers have more than 5% of their data missing:' + str(flagged_tickers))


	#Cleaning the data by interpolating the NaN values
	data.interpolate(method = 'linear', inplace = True)

	#print(data)

	#We're using log prices
	Close_prices = np.log(data[('Close')].to_numpy().T)

	#Calculate correlation coefficients between prices
	R = np.corrcoef(Close_prices)

	#Filter those with smaller correlation than critical value, and delete duplicates
	crit_indices = np.argwhere(R > critical_corrcoef)
	crit_indices = crit_indices[ crit_indices[:, 0]  < crit_indices[:, 1]  ]


	#Here we obtain hedge ratios and spreads between pairs

	spreads = []
	hedge_ratios = [0]*len(crit_indices)

	for i in range(len(crit_indices)):
		hedge_ratios[i] = np.polyfit(Close_prices[crit_indices[i][0]], Close_prices[crit_indices[i][1]], deg = 1)[0]
		spreads.append(Close_prices[crit_indices[i][0]] - hedge_ratios[i]*Close_prices[crit_indices[i][1]])


	#Perform and ADF test on obtained spreads, using the one with smallest AIC value.

	ADF_stats = [0]*len(crit_indices)

	found_pairs = []

	for i in range(len(crit_indices)):
		min_AIC = 0

		for order in range(1, max_ADF_order+1): #testing ADF regression order up to some set value

			adf_stat, AIC_test =  ADF(spreads[i], order)
			if AIC_test < min_AIC: ADF_stats[i] = adf_stat

		if ADF_stats[i] <= ADF_crit_values(len(spreads[i])):
			flag = ''
			if tickers[crit_indices[i][0]] in flagged_tickers:
				flag += str(tickers[crit_indices[i][0]]) + ' has more than 5% of their its data missing'
				if tickers[crit_indices[i][1]] in flagged_tickers:
					flag += ' ' + str(tickers[crit_indices[i][1]]) + ' has more than 5% of their its data missing'
			elif tickers[crit_indices[i][1]] in flagged_tickers:
				flag += str(tickers[crit_indices[i][1]]) + ' has more than 5% of their its data missing'
			if len(flag) == 0:
				flag = 'None'
			found_pairs.append([tickers[crit_indices[i][0]], tickers[crit_indices[i][1]], float(hedge_ratios[i]), start_date, end_date, interval, flag])

	df_found_pairs = pd.DataFrame(found_pairs, columns = ['Ticker1', 'Ticker2', 'HedgeRatio', 'StartDate', 'EndDate', 'Interval', 'Flags'])

	return df_found_pairs





