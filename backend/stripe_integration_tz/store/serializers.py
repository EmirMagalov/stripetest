from rest_framework import serializers
from decimal import Decimal
from .models import Item, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ItemsSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    price_with_discount = serializers.SerializerMethodField()
    discount_percent = serializers.SerializerMethodField()
    tax_info = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "image",
            "description",
            "price",
            "quantity",
            "price_with_discount",
            "tax_info",
            "discount_percent",
            "categories",
            "currency",
            "created_at",
        ]

    def get_price_with_discount(self, obj):
        if obj.discount:
            multiplier = Decimal(1 - (obj.discount.percent / 100))
            return round(obj.price * multiplier, 2)
        return obj.price

    def get_discount_percent(self, obj):
        if obj.discount:
            return obj.discount.percent
        return None

    def get_tax_info(self, obj):
        if obj.tax:
            price_after_discount = self.get_price_with_discount(obj)

            tax_amount = round(price_after_discount * (obj.tax.percent / 100), 2)

            total_with_tax = price_after_discount + tax_amount

            return {
                "name": obj.tax.name,
                "percent": obj.tax.percent,
                "tax_amount": tax_amount,
                "total_with_tax": total_with_tax,
            }
        return None

    def create(self, validated_data):
        return Item.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.save()
        return instance
