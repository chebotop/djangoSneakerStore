from django.test import TestCase
from django.urls import reverse, get_resolver
from .models import ShoeModel, Cart, CartItem
from django.core.management import call_command

for pattern in get_resolver().url_patterns:
    print(pattern)


class MyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'fixtures.json')


class CartTests(MyTestCase):
    def test_add_to_cart_with_existing_shoe(self):
        shoe = ShoeModel.objects.first()  # Получаем первый объект обуви из БД
        if not shoe:
            self.skipTest("Нет доступной обуви в БД для тестирования")

        # Создание POST-запроса для добавления обуви в корзину
        response = self.client.post(reverse('add_to_cart'), {'shoe_id': shoe.id})

        # Проверка, что запрос был успешно обработан
        self.assertEqual(response.status_code, 200)

        # Проверка, что обувь добавлена в корзину
        self.assertTrue(CartItem.objects.filter(shoe=shoe).exists())

