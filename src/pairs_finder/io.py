import pandas as pd
from pathlib import Path

def get_tickers(csv_path):
	path = Path(csv_path)

	if not path.exists():
		raise FileNotFoundError(f'Input file was not found: {csv_path}')

	df_tickers = pd.read_csv(path)

	if 'tickers' not in df_tickers.columns:
		raise ValueError('CSV must contain \'tickers\' column')

	if len(df_tickers['tickers']) == 0:
		raise ValueError('Tickers column is empty')

	return df_tickers['tickers'].dropna().unique().tolist()

def save_found_pairs(df, output_path):
	path = Path(output_path)
	path.parent.mkdir(parents = True, exist_ok = True)

	file_exists = path.exists()

	df.to_csv(path, index = False, mode = 'a', header = not file_exists)

