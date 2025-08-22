import sqlite3

def create_users_table():
    with sqlite3.connect('database.db') as con:
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT,
                language TEXT,
                product_count INTEGER DEFAULT 0
            )
        """)
        con.commit()

def create_products_table():
    with sqlite3.connect('database.db') as con:
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_name TEXT,
                product_price TEXT,
                product_description TEXT,
                product_photo TEXT,
                product_coder TEXT
            )
        """)
        con.commit()

create_users_table()
create_products_table()

def add_user_id(user_id):
    with sqlite3.connect('database.db') as con:
        cursor = con.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        con.commit()

def add_username(user_id, username):
    with sqlite3.connect('database.db') as con:
        cursor = con.cursor()
        cursor.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
        con.commit()

def add_language(user_id, language):
    with sqlite3.connect('database.db') as con:
        cursor = con.cursor()
        cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (language, user_id))
        con.commit()

def add_product(user_id, product_name, product_price, product_description, product_photo, product_coder):
    with sqlite3.connect('database.db') as con:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO products (user_id, product_name, product_price, product_description, product_photo, product_coder) VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, product_name, product_price, product_description, product_photo, product_coder))
        con.commit()

def get_user(user_id):
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_user_data(user_id):
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM products WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else None

def add_product_count(user_id):
    with sqlite3.connect('database.db') as con:
        cursor = con.cursor()
        cursor.execute("UPDATE users SET product_count = 0 WHERE user_id = ?", (user_id,))
        con.commit()

def update_product_count(user_id):
    with sqlite3.connect('database.db') as con:
        cursor = con.cursor()
        cursor.execute("UPDATE users SET product_count = product_count + 1 WHERE user_id = ?", (user_id,))
        con.commit()

def get_user_product_count(user_id):
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT product_count FROM users WHERE user_id = ?", (int(user_id),))
        row = cursor.fetchone()
        return dict(row)['product_count'] if row else None

def get_product_by_id(product_id):
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_all_users():
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return len([dict(row) for row in rows])

def get_all_products():
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        return len([dict(row) for row in rows])

# print(get_all_products())
# print(get_all_users())
# print(get_user_data(7077167971))
# print(get_user_data(7077167971))