import os
from dotenv import load_dotenv
from src.data import fetch_data, save_data_to_csv, load_data_from_csv
from src.analysis import detect_local_levels, filter_levels
from src.analysis.ai_interpreter import init_gemini, analyze_chart
from src.visualization import plot_with_levels_and_trend

# Load environment variables
load_dotenv()


def main(show_plot: bool = False, use_ai: bool = True):
    # Get Gemini API key from environment variables if AI is enabled
    if use_ai:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("Error: GEMINI_API_KEY not found in environment variables")
            return
        # Initialize Gemini
        init_gemini(api_key)

    symbol = "AAPL"
    start_date = "2022-01-01"
    end_date = "2024-05-01"
    interval = "1d"

    csv_file = f"{symbol}_data.csv"
    df = load_data_from_csv(csv_file)
    
    if df.empty:
        print(f"CSV'de veri yok veya hatalı, Yahoo Finance'ten çekiliyor: {symbol}")
        df = fetch_data(symbol, start_date, end_date, interval)
        if not df.empty:
            save_data_to_csv(df, csv_file)

    if not df.empty:
        # Generate and save the plot
        levels = detect_local_levels(df, window=5)
        levels = filter_levels(levels, rounding=2, top_n=2)
        print(levels.head())
        
        # Save the plot to a temporary file if needed for AI or showing
        plot_path = f"{symbol}_analysis.png" if (use_ai or show_plot) else None
        plot_with_levels_and_trend(df, levels, save_path=plot_path, show_plot=show_plot)
        
        if use_ai and plot_path:
            # Get AI interpretation
            print("\nGetting AI interpretation of the chart...")
            interpretation = analyze_chart(plot_path)
            print("\nAI Analysis:")
            print("-" * 50)
            print(interpretation)
            print("-" * 50)
            
            # Clean up the temporary file
            if os.path.exists(plot_path):
                os.remove(plot_path)
    else:
        print(f"{symbol} için veri işlenemedi.")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Stock Analysis with AI Interpretation')
    parser.add_argument('--no-plot', action='store_true', help='Run without displaying the plot')
    parser.add_argument('--no-ai', action='store_true', help='Run without AI interpretation')
    
    args = parser.parse_args()
    main(show_plot=not args.no_plot, use_ai=not args.no_ai)
