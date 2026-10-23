import pandas as pd
import matplotlib.pyplot as plt
from database import get_db_connection

def save_csv(df, filename):
    """Utility function to export dataframes to CSV."""
    df.to_csv(filename, index=False)
    print(f" Data exported to {filename}\n")


def sales_report():
    """Generates and exports a sales report."""
    conn = get_db_connection()
    query = """
    SELECT t.id, p.name, p.category, t.quantity, t.date
    FROM transactions t
    JOIN products p ON t.product_id = p.id
    WHERE t.type = 'sale'
    ORDER BY t.date DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()

    print("\n=== SALES REPORT ===")
    if df.empty:
        print("No sales records found.\n")
    else:
        print(df.to_string(index=False))
        save_csv(df, "sales_report.csv")


def purchase_report():
    """Generates and exports a purchase report."""
    conn = get_db_connection()
    query = """
    SELECT t.id, p.name, p.category, t.quantity, t.date
    FROM transactions t
    JOIN products p ON t.product_id = p.id
    WHERE t.type = 'purchase'
    ORDER BY t.date DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()

    print("\n=== PURCHASE REPORT ===")
    if df.empty:
        print("No purchase records found.\n")
    else:
        print(df.to_string(index=False))
        save_csv(df, "purchase_report.csv")


def stock_chart():
    """Generates a bar chart visualizing current stock levels across all products."""
    conn = get_db_connection()
    df = pd.read_sql("SELECT name, quantity FROM products", conn)
    conn.close()

    if df.empty:
        print("No stock data available to visualize.\n")
        return

    plt.figure(figsize=(10, 6))
    plt.bar(df['name'], df['quantity'], color='skyblue')
    plt.xlabel("Product Name")
    plt.ylabel("Stock Quantity")
    plt.title("Current Stock Levels")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def sales_trend_chart():
    """Generates a line graph showing sales volume trends over time."""
    conn = get_db_connection()
    query = """
    SELECT DATE(date) as day, SUM(quantity) as total_sales
    FROM transactions
    WHERE type = 'sale'
    GROUP BY day
    ORDER BY day ASC
    """
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        print("No sales transaction data available to plot.\n")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(df['day'], df['total_sales'], marker='o', linestyle='-', color='teal', label='Total Units Sold')
    plt.xlabel("Date")
    plt.ylabel("Units Sold")
    plt.title("Daily Sales Trend")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.show()