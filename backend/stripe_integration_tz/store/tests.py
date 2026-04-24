from django.test import TestCase
from django.urls import reverse
from store.models import Item

class PaymentTest(TestCase):
    def setUp(self):
        # Создаем тестовый товар
        self.item = Item.objects.create(name="Test Game", price=100,description='Test',quantity=10)

    def test_payment_url_exists(self):
        url = f"/api/v1/buy/{self.item.pk}/rub/"
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 404)
