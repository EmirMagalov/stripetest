from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
import stripe
from rest_framework.views import APIView

from .models import Item
from .serializers import ItemsSerializer
from config import get_config

stripe.api_key = get_config("STRIPE_SECRET_KEY")


def home(request):
    return HttpResponse("Hello, world.")


class ItemsAPI(APIView):
    def get(self, request):
        items = Item.objects.all()
        target_currency = request.query_params.get('currency', 'rub').lower()
        data = ItemsSerializer(items, context={'request': request}, many=True).data

        rate = 75.1
        total_in_rub = sum(item.get_final_price() for item in items)
        for item in data:
            price_in_rub = float(item['price'])
            discount_price_in_rub = float(item['price_with_discount'])

            if target_currency == 'usd':
                item['price'] = round(price_in_rub / rate, 2)
                item['price_with_discount'] = round(discount_price_in_rub / rate, 2)
                item['currency'] = 'usd'
            else:
                item['price'] = round(price_in_rub, 2)
                item['price_with_discount'] = round(discount_price_in_rub, 2)
                item['currency'] = 'rub'
        if target_currency == 'usd':
            total_sum = round(float(total_in_rub) / rate, 2)
        else:
            total_sum = round(float(total_in_rub), 2)
        return Response({
            "total_sum": total_sum,
            "items": data
        })

    def post(self, request):
        serializers = ItemsSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)

    def put(self, request, *args, **kwargs):
        pk = kwargs['pk']
        if not pk:
            return HttpResponse(status=404)
        try:
            instance = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        serializers = ItemsSerializer(instance=instance, data=request.data, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)


class CreateCheckoutSessionView(APIView):
    def get(self, request, pk=None, currency='rub'):
        if pk is None:
            currency = request.query_params.get('currency', 'rub').lower()
        if pk:
            items = Item.objects.filter(pk=pk)
        else:
            items = Item.objects.all()

        if not items.exists():
            return Response({"error": "Items not found"}, status=404)

        exchange_rate = 75.1
        line_items = []
        total_sum_with_tax = 0

        for item in items:

            multiplier = 1 - (item.discount.percent / 100) if item.discount else 1
            final_price_rub = float(item.price) * multiplier

            if currency == 'usd' and item.currency == 'rub':
                final_price = final_price_rub / exchange_rate
            elif currency == 'rub' and item.currency == 'usd':
                final_price = final_price_rub * exchange_rate
            else:
                final_price = final_price_rub

            final_price = round(final_price, 2)

            tax_rates = []
            tax_val = 0
            if item.tax and item.tax.stripe_tax_rate_id:
                tax_rates.append(item.tax.stripe_tax_rate_id)
                tax_val = round(final_price * (float(item.tax.percent) / 100), 2)

            total_sum_with_tax += (final_price + tax_val)

            line_items.append({
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': item.name,
                        'description': item.description[:100] if item.description else "",
                    },
                    'unit_amount': int(final_price * 100),
                },
                'quantity': 1,
                'tax_rates': tax_rates,
            })

        display_name = items[0].name if items.count() == 1 else "Cart Checkout"

        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            metadata={
                "items_count": items.count(),
            },
            success_url=(
                'http://localhost:5173/success'
                '?session_id={CHECKOUT_SESSION_ID}'
                f'&item_name={display_name}'
                f'&total_price={round(total_sum_with_tax, 2)}'
                f'&tax_percent={item.tax.percent if item.tax else 0}'
                f'&item_currency={currency}'
            ),
            cancel_url='http://localhost:5173/cancel/',
        )

        return Response({
            'id': session.id,
            'url': session.url
        })
