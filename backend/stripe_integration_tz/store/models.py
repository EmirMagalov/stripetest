from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название налога")
    percent = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Процент налога"
    )
    stripe_tax_rate_id = models.CharField(
        max_length=255, verbose_name="ID из панели Stripe"
    )

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"

    def __str__(self):
        return f"{self.name} ({self.percent}%)"


class Discount(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    percent = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name="Процент скидки",
    )

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def __str__(self):
        return f"{self.name} (-{self.percent}%)"


class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(
        upload_to="items/", null=True, blank=True, verbose_name="Фото"
    )
    quantity = models.IntegerField(verbose_name="Количесво")
    currency = models.CharField(default="rub", verbose_name="Валюта")
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Скидка",
    )
    tax = models.ForeignKey(
        Tax, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Налог"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(
        Category, related_name="items", verbose_name="Категория товара"
    )

    def get_final_price(self):
        if self.discount:
            multiplier = Decimal(1 - (self.discount.percent / 100))
            return round(self.price * multiplier, 2)
        return self.price

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name
