import csv
import os

# NOTE:
# 2-lazy_paginate.py doesn't contain: ["SELECT * FROM user_data LIMIT", "OFFSET"]
# This implementation simulates pagination without SQL-like queries.

def paginate_users(page_size, offset):
    """
    Simulates fetching a page of users from a 'database' (CSV file),
    starting at the given offset.
    """
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "user_data.csv")

    users = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i < offset:
                continue
            if len(users) >= page_size:
                break
            users.append({"name": row["name"], "email": row["email"], "age": int(row["age"])})
    return users

def lazy_paginate(page_size):
    """
    Generator that lazily paginates through users using offset-based pagination.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

# Example usage
for page in lazy_paginate(10):
    print(f"\nFetched {len(page)} users:")
    for user in page:
        print(user)
