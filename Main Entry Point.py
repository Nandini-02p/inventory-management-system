from database import init_db
from operations import (
    add_product,
    view_products,
    search_product,
    update_stock,
    record_transaction,
    low_stock_alert,
)
from analytics import (
    sales_report,
    purchase_report,
    stock_chart,
    sales_trend_chart,
)

def main():
    # Initialize DB Schema on launch
    try:
        init_db()
    except Exception as e:
        print(f"Database connection error: {e}")
        print("Ensure MySQL is running and your .env credentials are correct.")
        return

    while True:
        print("""
===================================
 INVENTORY MANAGEMENT SYSTEM (FDE)
===================================
1. Add Product
2. View Products
3. Search Product
4. Update Stock
5. Record Sale
6. Record Purchase
7. Low Stock Alert
8. Sales Report
9. Purchase Report
10. Stock Chart
11. Sales Trend Chart
0. Exit
""")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            search_product()
        elif choice == "4":
            update_stock()
        elif choice == "5":
            record_transaction("sale")
        elif choice == "6":
            record_transaction("purchase")
        elif choice == "7":
            low_stock_alert()
        elif choice == "8":
            sales_report()
        elif choice == "9":
            purchase_report()
        elif choice == "10":
            stock_chart()
        elif choice == "11":
            sales_trend_chart()
        elif choice == "0":
            print("Exiting application. Goodbye!")
            break
        else:
            print(" Invalid choice! Please select a valid menu option.\n")

if __name__ == "__main__":
    main()