from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    producer = models.CharField(max_length=255, default='Не указан')

    def __str__(self):
        return f'Id{self.id}: {self.name}'
