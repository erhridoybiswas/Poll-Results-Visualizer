import pandas as pd

def overall_summary(df):
    """Return overall vote counts and percentages."""
    counts = df["Answer"].value_counts().reset_index()
    counts.columns = ["Option", "Count"]
    total = counts["Count"].sum()
    counts["Percentage"] = (counts["Count"] / total * 100).round(1)
    return counts

def cross_tab_summary(df, group_col):
    """Return cross-tabulation of Answer vs group_col."""
    crosstab = pd.crosstab(df["Answer"], df[group_col], normalize='columns') * 100
    return crosstab.round(1)

def time_series_counts(df, freq='W'):
    """Count responses per week."""
    df_time = df.set_index("Date").resample(freq)["Answer"].count()
    return df_time