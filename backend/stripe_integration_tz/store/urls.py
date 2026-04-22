from django.urls import path, include
from .views import home, ItemsAPI, CreateCheckoutSessionView

urlpatterns = [
    path('', home, name='home'),
    path('api/v1/items/', ItemsAPI.as_view()),
    path('api/v1/items/<int:pk>/', ItemsAPI.as_view()),
    path('api/v1/buy/<int:pk>/<str:currency>/', CreateCheckoutSessionView.as_view()),
    path('api/v1/buy/', CreateCheckoutSessionView.as_view()),

]
