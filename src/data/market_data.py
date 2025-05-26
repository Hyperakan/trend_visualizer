import yfinance as yf
import pandas as pd

def fetch_data(symbol: str, start: str, end: str, interval: str = "1d") -> pd.DataFrame:
    try:
        df = yf.download(symbol,
                         start=start,
                         end=end,
                         interval=interval,
                         progress=True)
        if df.empty:
            raise ValueError(f"No data found for {symbol}")
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Missing required columns: {required_cols}")
        df = df[required_cols].apply(pd.to_numeric, errors='coerce')
        df.dropna(inplace=True)
        df.index = pd.to_datetime(df.index)
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()

def save_data_to_csv(df: pd.DataFrame, filename: str):
    df.to_csv(filename, index=True)
    print(f"Data saved to {filename}")

def load_data_from_csv(filename: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(filename, index_col=0)
        if df.empty:
            return df
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"CSV eksik sütunlar: {required_cols}")
        df = df[required_cols].apply(pd.to_numeric, errors='coerce')
        df.dropna(inplace=True)
        df.index = pd.to_datetime(df.index, errors='coerce')
        df.dropna(inplace=True)
        return df
    except Exception as e:
        print(f"Error loading data from {filename}: {e}")
        return pd.DataFrame()
