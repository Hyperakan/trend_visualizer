from src.data import fetch_data, save_data_to_csv, load_data_from_csv
from src.analysis import detect_local_levels, filter_levels
from src.visualization import plot_with_levels_and_trend


def main():
    symbol = "AAPL"
    start_date = "2022-01-01"
    end_date = "2024-01-01"
    interval = "1d"

    csv_file = f"{symbol}_data.csv"
    df = load_data_from_csv(csv_file)
    
    if df.empty:
        print(f"CSV'de veri yok veya hatalı, Yahoo Finance'ten çekiliyor: {symbol}")
        df = fetch_data(symbol, start_date, end_date, interval)
        if not df.empty:
            save_data_to_csv(df, csv_file)

    if not df.empty:
        levels = detect_local_levels(df, window=5)
        levels = filter_levels(levels, rounding=2, top_n=2)
        print(levels.head())
        plot_with_levels_and_trend(df, levels)
    else:
        print(f"{symbol} için veri işlenemedi.")


if __name__ == "__main__":
    main()
