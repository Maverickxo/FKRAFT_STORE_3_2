# import sqlite3
# from tabulate import tabulate
# import product_list
#
#
# def create_database_and_tables():
#     try:
#         conn = sqlite3.connect('ShopDB.db')
#
#         conn.execute('''CREATE TABLE IF NOT EXISTS products
#                      (id INTEGER PRIMARY KEY,
#                       name TEXT NOT NULL,
#                       price INTEGER NOT NULL,
#                       active INTEGER NOT NULL DEFAULT 1
#                       )''')
#         conn.execute('''CREATE TABLE IF NOT EXISTS coupons (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         coupon_code VARCHAR(10),
#                         discount_percentage DECIMAL(5, 2),
#                         off_time INTEGER DEFAULT 0
#                     )''')
#         conn.execute('''CREATE TABLE IF NOT EXISTS users (
#                         "id"	INTEGER,
#                         "user_id"	INTEGER NOT NULL,
#                         "block"	INTEGER DEFAULT 0,
#                         "ban"	INTEGER DEFAULT 0,
#                         "full_name"	TEXT,
#                         "money"	INTEGER NOT NULL DEFAULT 0,
#                         PRIMARY KEY("id" AUTOINCREMENT)
#                     )''')
#
#         conn.execute('''CREATE TABLE IF NOT EXISTS dice_rolls(
#                           user_id INTEGER PRIMARY KEY,
#                           last_roll_date TEXT,
#                           "user_name"	TEXT,
#                           "full_name"	TEXT
#                           )''')



#         print("База данных |ShopDB.db| таблицы и поля успешно созданы:")
#     except sqlite3.Error as e:
#         print("Ошибка:", e)
#
#     finally:
#         conn.close()
#
#
# def check_database_and_tables():
#     conn = sqlite3.connect('ShopDB.db')
#     cursor = conn.cursor()
#
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     tables = cursor.fetchall()
#
#     data = []
#     for count, table in enumerate(tables, 1):
#         cursor.execute(f"PRAGMA table_info({table[0]});")
#         columns = cursor.fetchall()
#         column_names = [column[1] for column in columns]
#         data.append([count, table[0], ', '.join(column_names)])
#
#     conn.close()
#
#     print(tabulate(data, headers=["#", "Таблица", "Поля"], tablefmt="pretty"))
#
# #
# # # #
# # # def insert_product(name, price):
# # #     conn = sqlite3.connect('ShopDB.db')
# # #     conn.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
# # #     conn.commit()
# # #     conn.close()
# # #
# # #
# # # for product in product_list.products:
# # #     name = product["name"]
# # #     price = product["price"]
# # #     insert_product(name, price)
