import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

def generate_poll_data(n=1000, seed=42):
    """Generate synthetic poll responses."""
    np.random.seed(seed)
    fake = Faker()
    
    # Poll question and options
    question = "Which feature should we prioritize next?"
    options = ["Dark Mode", "Export to PDF", "Mobile App", "API Access", "Real-time Sync"]
    
    # Regions and age groups
    regions = ["North", "South", "East", "West", "Central"]
    age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]
    genders = ["Male", "Female", "Other"]
    
    data = {
        "RespondentID": [fake.uuid4() for _ in range(n)],
        "Date": [fake.date_between(start_date='-30d', end_date='today') for _ in range(n)],
        "Question": [question] * n,
        "Answer": np.random.choice(options, n, p=[0.35, 0.25, 0.20, 0.12, 0.08]),
        "Region": np.random.choice(regions, n),
        "AgeGroup": np.random.choice(age_groups, n, p=[0.15, 0.30, 0.25, 0.20, 0.10]),
        "Gender": np.random.choice(genders, n, p=[0.48, 0.48, 0.04])
    }
    df = pd.DataFrame(data)
    # Add slight bias: e.g., "Mobile App" more popular in younger groups
    mask = (df["AgeGroup"].isin(["18-24", "25-34"])) & (df["Answer"] == "Mobile App")
    df.loc[mask, "Answer"] = np.random.choice(["Mobile App", "Dark Mode"], sum(mask), p=[0.7, 0.3])
    return df

if __name__ == "__main__":
    df = generate_poll_data(1500)
    df.to_csv("data/raw/poll_results.csv", index=False)
    print("Synthetic poll data generated: data/raw/poll_results.csv")