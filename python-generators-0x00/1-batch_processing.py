from itertools import islice
import csv
import os

def stream_users_in_batches(batch_size):
    """Generator that yields users from a CSV file in batches."""
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "user_data.csv")

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        batch = []
        for row in reader:
            user = {"name": row["name"], "email": row["email"], "age": int(row["age"])}
            batch.append(user)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

def batch_processing(batch_size):
    """Process users in batches and filter users over the age of 25."""
    for batch in stream_users_in_batches(batch_size):
        filtered = (user for user in batch if user["age"] > 25)
        print(f"Filtered users over 25 from batch of {len(batch)}:")
        for user in filtered:
            print(user)

batch_size = 50
batch_processing(batch_size)

