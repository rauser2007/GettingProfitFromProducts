import sqlite3

# Підключення до бази даних shop.db
conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

# Створення таблиці products, якщо вона не існує
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
);
""")

# Створення таблиці orders, якщо вона не існує
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")

# Заповнення таблиці products, якщо вона порожня
cursor.execute("SELECT COUNT(*) FROM products")
if cursor.fetchone()[0] == 0:
    cursor.executemany("INSERT INTO products (name, price) VALUES (?, ?)", [
        ('Laptop', 1200.00),
        ('Smartphone', 700.00),
        ('Headphones', 150.00),
        ('Tablet', 500.00)
    ])
    print("Таблиця products заповнена тестовими даними.")

# Заповнення таблиці orders, якщо вона порожня
cursor.execute("SELECT COUNT(*) FROM orders")
if cursor.fetchone()[0] == 0:
    cursor.executemany("INSERT INTO orders (product_id, quantity, customer_id) VALUES (?, ?, ?)", [
        (1, 5, 1),
        (2, 3, 2),
        (1, 2, 3),
        (3, 10, 1),
        (2, 8, 4),
        (4, 5, 3),
        (1, 3, 2),
        (3, 12, 1)
    ])
    print("Таблиця orders заповнена тестовими даними.")

# SQL-запит для отримання продуктів, замовлених більше 10 разів
query = """
SELECT 
    p.name AS product_name,
    SUM(o.quantity) AS total_quantity,
    SUM(o.quantity * p.price) AS total_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY o.product_id
HAVING SUM(o.quantity) > 10
ORDER BY total_quantity DESC;
"""

# Виведення SQL-запиту
print("\nSQL-запит:")
print(query)

# Виконання SQL-запиту
cursor.execute(query)
results = cursor.fetchall()

# Виведення результатів
print("\nРезультати:")
if results:
    for product_name, total_quantity, total_revenue in results:
        print(f"{product_name}: {total_quantity} шт., прибуток: ${total_revenue:.2f}")
else:
    print("Немає продуктів, замовлених більше 10 разів.")

# Закриття підключення
conn.commit()
conn.close()
print("\nЗ'єднання з базою даних закрито.")
