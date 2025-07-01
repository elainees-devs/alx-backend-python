# MySQL Data Seeder with Python Generator

## 📌 Objective

Create a Python script that **streams rows from an SQL database one by one** using a generator. This tool helps efficiently seed and access large datasets without loading everything into memory at once.

---

## 🛠️ Features

- Connects to a MySQL server
- Creates a database named `ALX_prodev` if it doesn't exist
- Creates a table `user_data` with:
  - `user_id` (Primary Key, UUID, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Populates the table using data from a CSV file: `user_data.csv`
- Skips duplicate entries
- Provides a foundation for building row-by-row data generators

---

## 📂 Project Structure

python-generators-0x00/
│
├── pycache/ # Python cache files
├── .env # Environment variables (MySQL credentials)
├── main.py # script to implement data generator logic
├── README.md # Project documentation (you're reading it!)
├── seed.py # Script to create DB, table, and insert CSV data
├── user_data.csv # Sample CSV with user records
└── venv/ # Python virtual environment

---

## 🧪 Function Prototypes

```python
def connect_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to the MySQL server (without specifying a database)."""

def create_database(connection: mysql.connector.connection.MySQLConnection):
    """Create the 'ALX_prodev' database if it doesn't exist."""

def connect_to_prodev() -> mysql.connector.connection.MySQLConnection:
    """Connect to the 'ALX_prodev' database."""

def create_table(connection: mysql.connector.connection.MySQLConnection):
    """Create the 'user_data' table with required schema if it doesn't exist."""

def insert_data(connection: mysql.connector.connection.MySQLConnection, data: List[Tuple]):
    """Insert rows into the user_data table, avoiding duplicates."""
````

---

## 📋 Prerequisites

* Python 3.8+
* MySQL Server (version 8.0 or higher recommended)
* Required Python packages:

  ```bash
  pip install mysql-connector-python python-dotenv
  ```

---

## 🔐 Environment Variables

Create a `.env` file in the project root to securely store credentials:

```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
```

> ✅ Remember to **add `.env` to `.gitignore`** to avoid pushing secrets.

---

## 🚀 Usage

1. Place your `user_data.csv` file in the project root.
2. Run the script:

```bash
python3 seed.py
```

This will:

* Connect to the MySQL server
* Create the `ALX_prodev` database and `user_data` table if not present
* Insert data from `user_data.csv` into the table

---

## 🧼 CSV Format

Ensure your `user_data.csv` uses the following structure (no header):

```
name,email,age
Alice,alice@example.com,23
Bob,bob@example.com,30
...
```

The `user_id` is automatically generated as a UUID inside the script.

---

## 🧠 Future Enhancements

* Add a row-by-row generator to stream user data
* Add unit tests for each function
* Dockerize the setup for consistent deployment

---

## 📄 License

This project is intended for educational purposes, especially in **Backend and DevOps learning paths**.

---

## 🙌 Acknowledgements

Created as part of the **ALX Pro Backend Program**.

```
