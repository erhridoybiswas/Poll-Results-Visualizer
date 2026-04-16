import pandas as pd
from src.data_generator import generate_poll_data
from src.data_cleaner import clean_poll_data
from src.analyzer import overall_summary, cross_tab_summary
from src.visualizer import plot_bar_overall, plot_pie_overall, plot_stacked_bar

def main():
    print("Generating synthetic poll data...")
    df_raw = generate_poll_data(1500)
    df_raw.to_csv("data/raw/poll_results.csv", index=False)
    
    print("Cleaning data...")
    df = clean_poll_data(df_raw)
    
    print("Analyzing...")
    summary = overall_summary(df)
    print("\nOverall Results:\n", summary)
    
    # Save charts
    plot_bar_overall(summary, "outputs/figures/overall_bar.png")
    plot_pie_overall(summary, "outputs/figures/overall_pie.png")
    
    crosstab_region = cross_tab_summary(df, "Region")
    plot_stacked_bar(crosstab_region, "outputs/figures/stacked_region.png")
    
    print("Analysis complete. Charts saved to outputs/figures/")

if __name__ == "__main__":
    main()