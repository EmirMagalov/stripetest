from rest_framework.views import APIView
from store.models import Item
from rest_framework.response import Response
import stripe
from config import get_config

stripe.api_key = get_config("STRIPE_SECRET_KEY")


class CreatePaymentIntentView(APIView):
    def get(self, request, pk=None, currency="rub"):
        if pk is None:
            currency = request.query_params.get("currency", "rub").lower()

        if pk:
            items = Item.objects.filter(pk=pk)
        else:
            items = Item.objects.all()

        if not items.exists():
            return Response({"error": "Items not found"}, status=404)

        exchange_rate = 75.1
        total_sum_with_tax = 0

        for item in items:
            multiplier = 1 - (item.discount.percent / 100) if item.discount else 1
            final_price_rub = float(item.price) * multiplier

            if currency == "usd" and item.currency == "rub":
                final_price = final_price_rub / exchange_rate
            elif currency == "rub" and item.currency == "usd":
                final_price = final_price_rub * exchange_rate
            else:
                final_price = final_price_rub

            final_price = round(final_price, 2)

            tax_val = 0
            if item.tax:
                tax_val = round(final_price * (float(item.tax.percent) / 100), 2)

            total_sum_with_tax += final_price + tax_val

        # Stripe работает в центах
        amount_in_cents = int(round(total_sum_with_tax * 100))
        total_sum_with_tax = round(float(total_sum_with_tax), 2)
        intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency=currency,
            metadata={
                "items_count": items.count(),
            },
        )

        return Response(
            {
                "client_secret": intent.client_secret,
                "total_sum": total_sum_with_tax,
                "item_name": items.first().name,
                "tax_percent": items.first().tax.percent if items.first().tax else 0,
            }
        )
