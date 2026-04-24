from django.contrib import admin
from .models import Item, Category, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "currency", "quantity", "discount", "tax")
    list_display_links = ("id", "name")
    search_fields = ("name", "description")
    list_filter = ("currency", "discount", "tax")
    list_editable = ("price", "quantity", "discount", "tax")


admin.site.register(Category)
admin.site.register(Discount)
admin.site.register(Tax)
