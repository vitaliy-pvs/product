import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

#  test_API   ****************************************************************************************************
from rest_framework import status

from store.models import Product
from store.serializers import ProductSerializer


class ProductApiTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user')
        self.product_1 = Product.objects.create(name='Prod_1', price=500, producer='Producer_1')
        self.product_2 = Product.objects.create(name='Prod_2', price=1000, producer='Producer_2')
        self.product_3 = Product.objects.create(name='Prod_3', price=2000, producer='Producer_2')

    def test_get(self):
        url = reverse('product-list')
        # url = '/product/'
        response = self.client.get(url)
        serializer_data = ProductSerializer([self.product_1, self.product_2, self.product_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('product-list')
        response = self.client.get(url, data={'search': 'Producer_2'})
        serializer_data = ProductSerializer([self.product_2, self.product_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Product.objects.all().count())
        url = reverse('product-list')
        data = {
            "name": "Колонки",
            "price": 2500,
            "producer": "Sven"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Product.objects.all().count())

    def test_update(self):
        url = reverse('product-detail', args=(self.product_1.id,))
        data = {
            "name": self.product_1.name,
            "price": 555,
            "producer": self.product_1.producer
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.product_1 = Product.objects.get(id=self.product_1.id) - или как ниже
        self.product_1.refresh_from_db()
        self.assertEqual(self.product_1.price, 555)



#  test_serializers  *****************************************************************************************


class ProductSerializerTestCase(TestCase):
    def setUp(self):
        self.product_1 = Product.objects.create(name='Prod_1', price=500, producer='Producer_1')
        self.product_2 = Product.objects.create(name='Prod_2', price=1000, producer='Producer_2')
        self.product_3 = Product.objects.create(name='Prod_3', price=2000, producer='Producer_3')

    def test_ok(self):
        data = ProductSerializer([self.product_1, self.product_2, self.product_3], many=True).data
        expected_data = [
            {
                'id': self.product_1.id,
                'name': 'Prod_1',
                'price': '500.00',
                'producer': 'Producer_1'
            },
            {
                'id': self.product_2.id,
                'name': 'Prod_2',
                'price': '1000.00',
                'producer': 'Producer_2'
            },
            {
                'id': self.product_3.id,
                'name': 'Prod_3',
                'price': '2000.00',
                'producer': 'Producer_3'
            }
        ]
        self.assertEqual(expected_data, data)
