# import sqlite3

# # Подключение к базе данных SQLite
# connection = sqlite3.connect('C:\\Users\\admin\\Documents\\website\\sneaker_store\\db.sqlite3')
# cursor = connection.cursor()

# # SQL-запрос для добавления столбца brand_id
# sql_query_brand = '''
#     ALTER TABLE main_shoemodel
#     ADD COLUMN brand_id INTEGER REFERENCES brand(id) ON DELETE CASCADE
# '''

# # SQL-запрос для добавления столбца size_id
# sql_query_size = '''
#     ALTER TABLE main_shoemodel
#     ADD COLUMN size_id INTEGER REFERENCES size(id) ON DELETE CASCADE
# '''

# # Выполнение SQL-запросов
# cursor.execute(sql_query_brand)
# cursor.execute(sql_query_size)

# # Сохранение изменений в базе данных
# connection.commit()

# # Закрытие соединения с базой данных
# connection.close()
