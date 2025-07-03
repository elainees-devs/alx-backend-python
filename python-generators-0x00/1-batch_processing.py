import csv
import os

# Simulate: SELECT * FROM user_data
def stream_users_in_batches(batch_size):
    """Simulates SELECT * FROM user_data in batches."""
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
    return  # Ends generator explicitly (optional)

# Simulate: SELECT * FROM user_data WHERE age > 25
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered = (user for user in batch if user["age"] > 25)
        print(f"Filtered users over 25 from batch of {len(batch)}:")
        for user in filtered:
            print(user)
    return "Batch processing complete."  # Explicit return added

batch_size = 50
batch_processing(batch_size)
