import csv
import os

# Generator: yields one user age at a time
def stream_user_ages():
    """Yields user ages from the CSV file one by one."""
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "user_data.csv")

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield int(row["age"])

# Calculate average age using the generator
def compute_average_age():
    total_age = 0
    count = 0
    for age in stream_user_ages(): 
        total_age += age
        count += 1

    average = total_age / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")

compute_average_age()
