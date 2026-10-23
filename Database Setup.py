import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """Establishes and returns a database connection using environment variables."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "inventory_db")
    )

def init_db():
    """Initializes the database and creates required tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Products Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        category VARCHAR(50) NOT NULL,
        quantity INT NOT NULL,
        price FLOAT NOT NULL
    )
    """)

    # Create Transactions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT NOT NULL,
        type VARCHAR(10) NOT NULL,
        quantity INT NOT NULL,
        date DATETIME NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()