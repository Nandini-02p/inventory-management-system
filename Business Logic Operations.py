from datetime import datetime
import pandas as pd
from database import get_db_connection

def add_product():
    """Adds a new product to the inventory database with input validation."""
    name = input("Product Name: ").strip()
    category = input("Category: ").strip()
    
    if not name or not category:
        print(" Error: Name and Category cannot be empty!\n")
        return

    try:
        qty = int(input("Quantity: "))
        price = float(input("Price: "))
        if qty < 0 or price < 0:
            print(" Error: Quantity and Price must be positive values!\n")
            return
    except ValueError:
        print(" Error: Invalid numeric input!\n")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, category, quantity, price) VALUES (%s, %s, %s, %s)",
        (name, category, qty, price)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(" Product added successfully!\n")


def view_products():
    """Displays all current products in the inventory."""
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM products", conn)
    conn.close()

    print("\n=== INVENTORY ===")
    if df.empty:
        print("No products available.\n")
    else:
        print(df.to_string(index=False))
        print()


def search_product():
    """Searches products by name or category using parameterized queries."""
    keyword = input("Enter name or category to search: ").strip()
    if not keyword:
        print(" Error: Search term cannot be empty!\n")
        return

    conn = get_db_connection()
    query = "SELECT * FROM products WHERE name LIKE %s OR category LIKE %s"
    search_term = f"%{keyword}%"
    df = pd.read_sql(query, conn, params=(search_term, search_term))
    conn.close()

    print("\n=== SEARCH RESULTS ===")
    if df.empty:
        print("No matching records found.\n")
    else:
        print(df.to_string(index=False))
        print()


def update_stock():
    """Updates existing product stock levels safely."""
    view_products()
    try:
        product_id = int(input("Product ID to update: "))
        qty = int(input("Quantity adjustment (+ to add / - to remove): "))
    except ValueError:
        print(" Error: Input must be a valid integer!\n")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT quantity FROM products WHERE id = %s", (product_id,))
    result = cursor.fetchone()
    
    if not result:
        print(" Error: Product ID not found!\n")
        cursor.close()
        conn.close()
        return

    current_stock = result[0]
    if current_stock + qty < 0:
        print(" Error: Stock level cannot drop below zero!\n")
        cursor.close()
        conn.close()
        return

    cursor.execute("UPDATE products SET quantity = quantity + %s WHERE id = %s", (qty, product_id))
    conn.commit()
    cursor.close()
    conn.close()
    print(" Stock updated successfully!\n")


def record_transaction(transaction_type):
    """Records a sale or purchase transaction and updates stock levels."""
    view_products()
    try:
        product_id = int(input("Product ID: "))
        qty = int(input("Quantity: "))
        if qty <= 0:
            print(" Error: Quantity must be greater than zero!\n")
            return
    except ValueError:
        print(" Error: Input must be a valid integer!\n")
        return

    conn = get_db_connection()
    cursor = cursor = conn.cursor()

    cursor.execute("SELECT quantity FROM products WHERE id = %s", (product_id,))
    result = cursor.fetchone()

    if not result:
        print(" Error: Product ID not found!\n")
        cursor.close()
        conn.close()
        return

    stock = result[0]

    if transaction_type == "sale":
        if qty > stock:
            print(" Error: Insufficient stock available!\n")
            cursor.close()
            conn.close()
            return
        cursor.execute("UPDATE products SET quantity = quantity - %s WHERE id = %s", (qty, product_id))
    else:
        cursor.execute("UPDATE products SET quantity = quantity + %s WHERE id = %s", (qty, product_id))

    cursor.execute(
        "INSERT INTO transactions (product_id, type, quantity, date) VALUES (%s, %s, %s, %s)",
        (product_id, transaction_type, qty, datetime.now())
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f" {transaction_type.capitalize()} recorded successfully!\n")


def low_stock_alert(limit=5):
    """Displays products falling below a defined stock threshold."""
    conn = get_db_connection()
    query = "SELECT * FROM products WHERE quantity <= %s"
    df = pd.read_sql(query, conn, params=(limit,))
    conn.close()

    if df.empty:
        print(" No low-stock items found.\n")
    else:
        print("\n LOW STOCK ALERT")
        print(df.to_string(index=False))
        print()