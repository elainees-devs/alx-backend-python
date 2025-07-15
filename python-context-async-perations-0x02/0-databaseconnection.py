# execute_query.py

from db_connection import DatabaseConnection

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.results = None

    def __enter__(self):
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(self.query, self.params)
            self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

# Usage example
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("users.db", query, params) as results:
    print("Results:", results)
