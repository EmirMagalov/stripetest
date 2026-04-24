from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from config import get_config


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = get_config("STRIPE_WEBHOOK_SECRET")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        print(f"💰 ОПЛАТА УСПЕШНА! Сумма: {payment_intent.amount / 100}")

    return HttpResponse(status=200)
