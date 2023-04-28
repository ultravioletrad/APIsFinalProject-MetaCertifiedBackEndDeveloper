from rest_framework import serializers
from django.contrib.auth.models import User
from decimal import Decimal

from .models import Category, MenuItem, Cart, Order, OrderItem,CartOrder


class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
    queryset=Category.objects.all()
     )
    #category = CategorySerializer()
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'unit_price', 'category', 'featured_item']
    

class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    
    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'price': {'required': False},
        }

    def validate(self, attrs):
        menuitem = attrs.get('menuitem')
        if menuitem:
            attrs['unit_price'] = menuitem.unit_price
        attrs['price'] = attrs['quantity'] * attrs['unit_price']
        return attrs

    def get_price(self, obj):
        return obj.price

# Here, we've added a unit_price field to the CartSerializer, and set it to write_only=True, which means it's only used when creating or updating a Cart object, and won't be included in the response.

# In the validate method, we first check if a menuitem object is included in the request payload. If it is, we set the unit_price attribute to the unit_price of the menuitem object. We then calculate the price attribute based on the quantity and unit_price.



    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):

    orderitem = OrderItemSerializer(many=True, read_only=True, source='order')

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew',
                  'status', 'date', 'total', 'orderitem']


class UserSerilializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

class CartOrderSerializer(serializers.ModelSerializer):
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    #user = serializers.ReadOnlyField(source='user.username')
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = CartOrder
        fields = '__all__'

