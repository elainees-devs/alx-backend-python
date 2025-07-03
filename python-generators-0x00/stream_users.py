import csv
import os

def stream_users():
    """Generator that yields users from a CSV file line by line."""
    # Get path relative to this file
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "user_data.csv")

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield {"name": row["name"], "email": row["email"], "age": int(row["age"])}
