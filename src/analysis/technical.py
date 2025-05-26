import pandas as pd
from scipy.signal import find_peaks

def detect_local_levels(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    highs = df['High'].astype(float).to_numpy()
    lows = df['Low'].astype(float).to_numpy()
    peaks, _ = find_peaks(highs, distance=window)
    valleys, _ = find_peaks(-lows, distance=window)
    records = []
    for idx in peaks:
        records.append({'index': df.index[idx], 'level': highs[idx], 'type': 'resistance'})
    for idx in valleys:
        records.append({'index': df.index[idx], 'level': lows[idx], 'type': 'support'})
    return pd.DataFrame(records)

def filter_levels(levels: pd.DataFrame, rounding: int = 2, top_n: int = 2) -> pd.DataFrame:
    levels['rounded'] = levels['level'].round(rounding)
    count_df = levels.groupby(['rounded', 'type']).size().reset_index(name='count')
    top_levels = count_df.sort_values(by='count', ascending=False).groupby('type').head(top_n)
    filtered = levels.merge(top_levels[['rounded', 'type']], on=['rounded', 'type'])
    return filtered.drop(columns=['rounded'])

def find_most_separated_pair(indexes):
    pairs = [(i, j) for i in indexes for j in indexes if j > i]
    if not pairs:
        return None, None
    return max(pairs, key=lambda p: p[1] - p[0])
