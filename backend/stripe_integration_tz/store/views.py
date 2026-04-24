from django.http import HttpResponse
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import Item
from .serializers import ItemsSerializer
from config import get_config

frontend_url = get_config("FRONTEND_URL")


class ItemsAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            item = get_object_or_404(Item, pk=pk)
            items_queryset = [item]
        else:
            items_queryset = Item.objects.all()
        target_currency = request.query_params.get("currency", "rub").lower()
        data = ItemsSerializer(items_queryset, many=True).data

        rate = 75.1
        total_in_rub = sum(item.get_final_price() for item in items)
        for item in data:
            price_in_rub = float(item["price"])
            discount_price_in_rub = float(item["price_with_discount"])

            if target_currency == "usd":
                item["price"] = round(price_in_rub / rate, 2)
                item["price_with_discount"] = round(discount_price_in_rub / rate, 2)
                item["currency"] = "usd"
            else:
                item["price"] = round(price_in_rub, 2)
                item["price_with_discount"] = round(discount_price_in_rub, 2)
                item["currency"] = "rub"
        if target_currency == "usd":
            total_sum = round(float(total_in_rub) / rate, 2)
        else:
            total_sum = round(float(total_in_rub), 2)
        return Response({"total_sum": total_sum, "items": data})

    def post(self, request):
        serializers = ItemsSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)

    def put(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        if not pk:
            return HttpResponse(status=404)
        try:
            instance = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        serializers = ItemsSerializer(
            instance=instance, data=request.data, partial=True
        )
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)
