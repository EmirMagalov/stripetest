from django.urls import path
from .views import ItemsAPI

# from store.payments.webhooks import stripe_webhook

urlpatterns = [
    path("api/v1/items/", ItemsAPI.as_view()),
    path("api/v1/items/<int:pk>/", ItemsAPI.as_view()),
]
