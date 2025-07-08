import sqlite3

# Define the custom context manager
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        print("Opening database connection...")
        self.connection = sqlite3.connect(self.db_name)
        return self.connection  # Makes the connection object available in the with block

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

with DatabaseConnection("users.db") as conn:
    cursor = conn.cursor()
    # Create a table if it doesn't exist
    cursor.execute('''
        SELECT * FROM users
    ''')
    users = cursor.fetchall()
    print("Users:", users)  