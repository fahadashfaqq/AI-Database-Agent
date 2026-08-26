import sqlite3
from pathlib import Path

BASE_DIR =Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "users.db"

def get_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection

def init_db():

    connection = get_connection()

    data = connection.cursor()

    #admin table
    data.execute(
        """
        CREATE TABLE IF NOT EXISTS admins(id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL UNIQUE)
        """
        )


    #users table 
    data.execute(
         """
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT,
        city TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        """

    )

    #add a test admin

    data.execute(
        """
        INSERT OR IGNORE INTO admins (email) VALUES(?)""",("admin@example.com",)
        )

    connection.commit()

    data.close()
    connection.close()