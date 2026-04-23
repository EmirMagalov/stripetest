from django.urls import path, include
from .views import home, ItemsAPI, CreatePaymentIntentView
from .webhooks import stripe_webhook

urlpatterns = [
    path("", home, name="home"),
    path("api/v1/items/", ItemsAPI.as_view()),
    path("api/v1/items/<int:pk>/", ItemsAPI.as_view()),
    path("api/v1/buy/<int:pk>/<str:currency>/", CreatePaymentIntentView.as_view()),
    path("api/v1/buy/", CreatePaymentIntentView.as_view()),
    path("webhook/stripe/", stripe_webhook, name="stripe_webhook"),
]
