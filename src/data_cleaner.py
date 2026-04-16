import pandas as pd

def clean_poll_data(df):
    """Clean poll DataFrame: drop nulls, standardize text."""
    # Drop rows with any missing critical columns
    df_clean = df.dropna(subset=["Answer", "Region", "AgeGroup", "Gender"]).copy()
    
    # Standardize text columns (strip whitespace, title case)
    text_cols = ["Answer", "Region", "AgeGroup", "Gender"]
    for col in text_cols:
        df_clean[col] = df_clean[col].str.strip().str.title()
    
    # Convert Date to datetime
    df_clean["Date"] = pd.to_datetime(df_clean["Date"])
    
    return df_clean

if __name__ == "__main__":
    df_raw = pd.read_csv("data/raw/poll_results.csv")
    df_clean = clean_poll_data(df_raw)
    df_clean.to_csv("data/processed/poll_results_clean.csv", index=False)
    print("Cleaned data saved.")