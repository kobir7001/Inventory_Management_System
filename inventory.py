import sqlite3
from datetime import datetime

# Database file
DATABASE_FILE = "inventory.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
   
    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            name TEXT PRIMARY KEY,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Purchases (
            transaction_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (name) REFERENCES Products(name)
        )
    ''')
   
    conn.commit()
    conn.close()

# Add a new product
def add_product(name, price, quantity):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
   
    try:
        cursor.execute('''
            INSERT INTO Products (name, price, quantity)
            VALUES (?, ?, ?)
        ''', (name, price, quantity))
       
        conn.commit()
        print("Product '" + name + "' added successfully.")
    except sqlite3.IntegrityError:
        print("Product with name " + name + " already exists.")
    finally:
        conn.close()

# Update product quantity
def update_product_quantity(name, quantity):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
   
    cursor.execute('''
        UPDATE Products
        SET quantity = quantity + ?
        WHERE name = ?
    ''', (quantity, name))
   
    if cursor.rowcount > 0:
        conn.commit()
        print("Quantity for product " + name + " updated successfully.")
    else:
        print("Product with name " + name + " not found.")
   
    conn.close()

# Make a purchase
def make_purchase(name, quantity):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
   
    # Check product availability
    cursor.execute('''
        SELECT price, quantity FROM Products WHERE name = ?
    ''', (name,))
    product = cursor.fetchone()
   
    if product:
        price, available_quantity = product
        if available_quantity >= quantity:
            # Update product quantity
            cursor.execute('''
                UPDATE Products
                SET quantity = quantity - ?
                WHERE name = ?
            ''', (quantity, name))
           
            # Log purchase
            transaction_id = "txn" + datetime.now().strftime('%Y%m%d%H%M%S')
            total_price = price * quantity
            timestamp = datetime.now().isoformat()
           
            cursor.execute('''
                INSERT INTO Purchases (transaction_id, name, quantity, total_price, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (transaction_id, name, quantity, total_price, timestamp))
           
            conn.commit()
            print("Purchase successful. " + str(quantity) + "x " + name + " sold.")
        else:
            print("Insufficient stock for product " + name + ".")
    else:
        print("Product with name " + name + " not found.")
   
    conn.close()

# Display products
def display_products():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
   
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
   
    if not products:
        print("No products available.")
    else:
        print("Product Catalog:")
        for product in products:
            print("Name: " + product[0] + ", Price: ₹" + str(product[1]) + ", Quantity: " + str(product[2]))
   
    conn.close()

# Display purchase history
def display_purchase_history():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
   
    cursor.execute('SELECT * FROM Purchases')
    purchases = cursor.fetchall()
   
    if not purchases:
        print("No purchase history available.")
    else:
        print("Purchase History:")
        for purchase in purchases:
            print("Transaction ID: " + purchase[0] + ", Name: " + purchase[1] + ", Quantity: " + str(purchase[2]) + ", Total Price: ₹" + str(purchase[3]) + ", Timestamp: " + purchase[4])
   
    conn.close()

# Main function
def main():
    init_db()
   
    while True:
        print("\nInventory Management System")
        print("1. Add Product")
        print("2. Modify Product Quantity")
        print("3. Make Purchase")
        print("4. Display Stock")
        print("5. Purchase History")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter product name: ")
            price = float(input("Enter price: "))
            quantity = int(input("Enter quantity: "))
            add_product(name, price, quantity)

        elif choice == "2":
            name = input("Enter product name: ")
            quantity = int(input("Enter quantity to add/subtract(+ve to add & -ve to remove): "))
            update_product_quantity(name, quantity)

        elif choice == "3":
            name = input("Enter product name: ")
            quantity = int(input("Enter quantity to purchase: "))
            make_purchase(name, quantity)

        elif choice == "4":
            display_products()

        elif choice == "5":
            display_purchase_history()

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()