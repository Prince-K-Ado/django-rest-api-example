from collections import OrderedDict
from .models import Item , Order
from rest_framework_json_api import serializers
from rest_framework import status
from rest_framework.exceptions import APIException




class NotEnoughStockException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'There is not enough stock'
    default_code = 'invalid'




class ItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields = (
            'title',
            'stock',
            'price',
        )




class OrderSerializer(serializers.ModelSerializer):

    item = serializers.PrimaryKeyRelatedField(queryset = Item.objects.all(), many=False)
    
    class Meta:
        model = Order
        fields = (
            'item',
            'quantity',
        )

    def validate(self, res: OrderedDict):
        '''
        Used to validate Item stock levels
        '''
        item = res.get("item")
        quantity = res.get("quantity")
        if not item.check_stock(quantity):
            raise NotEnoughStockException
        return res
```
3) Register - Let's go ahead and register our new models to the built in admin pages. Open /ecommerce/admin.py and paste in the following code.

```
from django.contrib import admin
from . import models


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'item')