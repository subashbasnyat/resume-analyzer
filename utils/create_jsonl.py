import pandas as pd
import json

# input_file = 'data/skills_list.csv'
# input_file = 'data/job_title.csv'
input_file = "data/degrees.csv"

# output_file = 'data/skills.jsonl'
# output_file = 'data/job_title.jsonl'
output_file = "data/degrees.jsonl"


# column = 'skill_name'
# column = 'job_title'
column = "degree_title"

# label = 'SKILL'
# label = 'JOB'
label = "DEGREE"


df = pd.read_csv(input_file)


# Function to convert csv to the required pattern structure
def convert_to_pattern(column_name):
    if any(char.isdigit() for char in column_name):
        return None

    words = column_name.strip().split()

    # Prepare pattern for uppercase value (TEXT attribute)
    if any(word.isupper() for word in words):  # If skill contains uppercase words
        # Use the uppercase words as TEXT
        pattern = [{"TEXT": word.upper()} for word in words if word.isupper()]
    else:
        # If no uppercase words, break the skill into lowercase words
        pattern = [{"LOWER": word.lower()} for word in words]

    # Return the formatted structure
    return {"label": label, "pattern": pattern}


# Apply the conversion function to each value in the dataframe
converted_pattern = [convert_to_pattern(row) for row in df[column]]

# Filter out None values (skills containing numbers)
converted_pattern = [row for row in converted_pattern if row is not None]

# Using a set to track duplicates
seen_patterns = set()

# Save the results to a .jsonl file without duplicates
with open(output_file, "w") as f:
    for row in converted_pattern:
        # Convert the pattern to a string to check for duplicates
        pattern_str = json.dumps(row, sort_keys=True)

        if pattern_str not in seen_patterns:
            f.write(pattern_str + "\n")
            seen_patterns.add(pattern_str)

print(f"Data saved to {output_file}")
