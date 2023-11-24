from django.test import TestCase
from django.urls import reverse
from .models import ShoeModel, Cart, CartItem

class CartTests(TestCase):
    def setUp(self):
        # Создание тестовой обуви
        self.shoe = ShoeModel.objects.create(...)

        # Другие необходимые настройки для теста

    def test_add_to_cart(self):
        # ID созданной обуви
        shoe_id = self.shoe.id

        # Создание POST-запроса для добавления обуви в корзину
        response = self.client.post(reverse('add_to_cart'), {'shoe_id': shoe_id, 'selected_size': '42'})

        # Проверка, что запрос был успешно обработан
        self.assertEqual(response.status_code, 200)

        # Проверка, что обувь добавлена в корзину
        self.assertTrue(CartItem.objects.filter(shoe_id=shoe_id).exists())

        # Дополнительные проверки (например, правильно ли добавлен размер)
