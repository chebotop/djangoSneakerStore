from django.test import TestCase
from django.urls import reverse
from main.models import Cart, Brand, ShoeModel  # Замените `your_app` на имя вашего приложения

class CatalogPageTest(TestCase):
    def setUp(self):
        # Создание тестовых объектов
        self.cart = Cart.objects.create(total=0)
        self.brand = Brand.objects.create(name="Test Brand")
        self.shoe_model = ShoeModel.objects.create(brand=self.brand, model="Test Model", price=100.00)
        # Добавьте другие объекты, если необходимо

    def test_view_properties(self):
        # Создание запроса GET к вашему представлению
        url = reverse('catalog_page_all')  # Замените `catalog_page` на имя вашего представления
        response = self.client.get(url)

        # Проверка свойств объектов в ответе
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['cart'], self.cart)
        self.assertEqual(response.context['all_brands'].count(), 1)
        self.assertEqual(response.context['all_models'].count(), 1)
        # Добавьте другие проверки, если необходимо

