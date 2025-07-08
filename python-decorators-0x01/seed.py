import sqlite3
import csv

# Connect to SQLite database (or create it)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Step 1: Create the table (if not exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    name TEXT,
    email TEXT,
    age INTEGER DEFAULT 0
)
""")

# Step 2: Open the CSV file
with open("user_data.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    
    # Step 3: Insert each row into the table
    for row in csv_reader:
        cursor.execute("""
            INSERT OR REPLACE INTO users (name, email, age)
            VALUES (:name, :email, :age)
        """, row)

# Commit changes and close connection
conn.commit()
conn.close()
