from .Find_Pairs import find_pairs
from .io import get_tickers, save_found_pairs
import argparse

def main():
	parser = argparse.ArgumentParser( description = 'Find cointegrated asset pairs from CSV tickers list')

	parser.add_argument("--input", required = True, help = 'Path to CSV with tickers')
	parser.add_argument("--output", required = True, help = 'Output CSV file')
	parser.add_argument("--corr_threshold", type = float, default = 0.8, help = 'Minimal correlation threshold for assets')
	parser.add_argument("--start_date", type = str, default = None, help = 'Start date for data download')
	parser.add_argument("--end_date", type = str, default = None, help = 'End date for data download')
	parser.add_argument("--interval", type = str, default = '1d' , help = 'Time interval between data points. Available values: {1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo}')

	args = parser.parse_args()

	tickers = get_tickers(args.input)

	df_found_pars = find_pairs(
		tickers,
		critical_corrcoef = args.corr_threshold,
		start_date = args.start_date,
		end_date = args.end_date,
		interval = args.interval
	)

	if len(df_found_pars) == 0:
		print('No valid pairs were found')
	else:

		save_found_pairs(df_found_pars, args.output)

		print(f'Saved {len(df_found_pars)} pairs to {args.output}')

if __name__ == "__main__":
    main()

