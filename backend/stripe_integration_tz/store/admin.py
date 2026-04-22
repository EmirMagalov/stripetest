from django.contrib import admin

from .models import Item, Category,Discount,Tax

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Discount)
admin.site.register(Tax)
