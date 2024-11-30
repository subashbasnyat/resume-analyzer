import pandas as pd
import re

# Read the CSV file
df = pd.read_csv("data/job_title.old.csv")

df["job_title"] = df["job_title"].apply(
    lambda x: None if isinstance(x, str) and re.match(r"^\d+\.", x) else x
)

# Drop rows with None in the 'job_title' column
df = df.dropna(subset=["job_title"])

# Save the cleaned data back to a CSV
df.to_csv("data/job_title.csv", index=False)

print("Job titles cleaned and saved to 'data/job_title.csv'")
