from django.test import TestCase, Client
from django.urls import reverse
from .main import *

class AjaxTest(TestCase):
    def test_ajax_request(self):
        client = Client(HTTP_AJAX_REQUEST='true')
        response = client.get(reverse('catalog_page'))  # Используйте reverse для получения URL из имени представления
        self.assertEqual(response.status_code, 200)
        self.assertTrue('html' in response.json())  # Проверьте, что ответ содержит ключ 'html'

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
