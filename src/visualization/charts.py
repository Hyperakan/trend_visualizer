import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
from scipy.signal import find_peaks
from src.analysis.technical import find_most_separated_pair

def plot_with_levels_and_trend(df: pd.DataFrame, levels: pd.DataFrame, save_path: str = None, show_plot: bool = False):
    fig, ax = plt.subplots(figsize=(14, 8))
    df['Date'] = df.index
    df.reset_index(drop=True, inplace=True)

    mpf.plot(df.set_index('Date'), type='candle', ax=ax, style='yahoo', volume=False, show_nontrading=True)

    for _, row in levels.iterrows():
        color = 'green' if row['type'] == 'support' else 'red'
        linestyle = '-.' if row['type'] == 'support' else '--'
        ax.axhline(row['level'], linestyle=linestyle, color=color, linewidth=1)

    low_idxs, _ = find_peaks(-df['Low'].values, distance=5)
    high_idxs, _ = find_peaks(df['High'].values, distance=5)

    l1, l2 = find_most_separated_pair(low_idxs)
    h1, h2 = find_most_separated_pair(high_idxs)

    _plot_trend_lines(ax, df, l1, l2, h1, h2)
    _plot_breakouts(ax, df, l1, l2, h1, h2)

    ax.set_title("Destek/Direnç + Trend Kanalı")
    ax.set_xlabel("Tarih")
    ax.set_ylabel("Fiyat")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    plt.grid(True)
    plt.tight_layout()
    
    # Save the plot if save_path is provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show_plot:
        plt.show()
    else:
        plt.close()

def _plot_trend_lines(ax, df, l1, l2, h1, h2):
    if l1 is not None:
        ax.plot([df['Date'][l1], df['Date'][l2]], [df['Low'][l1], df['Low'][l2]],
                color='blue', linewidth=1.5, label='Alt Trend')

    if h1 is not None:
        ax.plot([df['Date'][h1], df['Date'][h2]], [df['High'][h1], df['High'][h2]],
                color='blue', linestyle='--', linewidth=1.5, label='Üst Trend')

def _plot_breakouts(ax, df, l1, l2, h1, h2):
    if l1 is not None:
        _plot_lower_breakout(ax, df, l1, l2)

    if h1 is not None:
        _plot_upper_breakout(ax, df, h1, h2)

def _plot_lower_breakout(ax, df, l1, l2):
    x1, x2 = mdates.date2num(df['Date'][l1]), mdates.date2num(df['Date'][l2])
    y1, y2 = df['Low'][l1], df['Low'][l2]
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    found = False
    for i in range(l2 + 1, len(df)):
        xi = mdates.date2num(df['Date'][i])
        yi = df['Low'][i]
        trend_y = m * xi + b
        if yi < trend_y:
            ax.annotate("Trend kırılımı", xy=(df['Date'][i], yi), xytext=(df['Date'][i], yi + 10),
                        arrowprops=dict(facecolor='red', shrink=0.05),
                        bbox=dict(boxstyle="round,pad=0.3", fc="lightgray", ec="gray"))
            found = True
            break

    if not found:
        _plot_potential_breakout(ax, df, l2, m, b)

def _plot_potential_breakout(ax, df, l2, m, b):
    min_dist = float('inf')
    best_idx = None
    for i in range(l2 + 1, len(df)):
        xi = mdates.date2num(df['Date'][i])
        yi = df['Low'][i]
        trend_y = m * xi + b
        dist = abs(yi - trend_y)
        if dist < min_dist:
            min_dist = dist
            best_idx = i

    if best_idx:
        ax.annotate("Olası kırılım", xy=(df['Date'][best_idx], df['Low'][best_idx]),
                    xytext=(df['Date'][best_idx], df['Low'][best_idx] + 10),
                    arrowprops=dict(facecolor='orange', shrink=0.05),
                    bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", ec="orange"))

def _plot_upper_breakout(ax, df, h1, h2):
    x1, x2 = mdates.date2num(df['Date'][h1]), mdates.date2num(df['Date'][h2])
    y1, y2 = df['High'][h1], df['High'][h2]
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    for i in range(h2 + 1, len(df)):
        xi = mdates.date2num(df['Date'][i])
        yi = df['High'][i]
        trend_y = m * xi + b
        if yi > trend_y:
            ax.annotate("Üst trend kırılımı", xy=(df['Date'][i], yi), xytext=(df['Date'][i], yi + 10),
                        arrowprops=dict(facecolor='green', shrink=0.05),
                        bbox=dict(boxstyle="round,pad=0.3", fc="lightgreen", ec="green"))
            break
