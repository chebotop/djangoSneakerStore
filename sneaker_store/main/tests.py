from django.test import TestCase
from django.urls import reverse
from .models import ShoeModel, ShoeBrand, Cart, ShoeColor
from django.shortcuts import get_object_or_404

class ShoePageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные для бренда и цвета
        brand = ShoeBrand.objects.create(name="Test Brand")
        color = ShoeColor.objects.create(color="Test Color")

        # Теперь создаем обувь с указанием цвета
        ShoeModel.objects.create(model="Test Shoe", brand=brand, color=color, sizes={"women": {"36EUR": "22.5см"}}, price="1000")

    def test_shoe_page_get_request(self):
        # Получаем первый объект обуви из базы данных
        shoe = ShoeModel.objects.first()
        
        # Отправляем GET-запрос на страницу обуви
        response = self.client.get(reverse('shoe_page', args=[shoe.id]))

        # Проверяем, что страница успешно загружена
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, shoe.model)

    def test_shoe_page_post_request_add_to_cart(self):
        # Получаем первый объект обуви и создаем корзину
        shoe = ShoeModel.objects.first()
        cart = Cart.objects.create(total=0)

        # Создаем сессию для корзины
        session = self.client.session
        session['cart_id'] = cart.id
        session.save()

        # Отправляем POST-запрос на добавление обуви в корзину
        response = self.client.post(reverse('shoe_page', args=[shoe.id]), {
            'selected_size': '36EUR'
        })

        # Проверяем, что запрос был успешно обработан
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cart.items.filter(shoe=shoe).exists())

