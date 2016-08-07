from django.contrib import admin
from django import forms
from inventory.models import *
from inventory.constants import *

class InventoryAdmin(admin.ModelAdmin):
	list_display = ('product_model', 'product_color', 'current_quantity')
	ordering = ['product_model', 'product_color']


class ProductAdmin(admin.ModelAdmin):
	list_display = ('model', 'color', 'suggested_price', 'cost')
	ordering = ['model', 'color']

class InventoryOrderAdmin(admin.ModelAdmin):
	list_display = ('manager', 'item', 'quantity', 'datetime', 'arrived')
	ordering = ('-datetime')


class ItemSoldAdmin(admin.ModelAdmin):
	list_display = ('user', 'item', 'quantity', 'datetime', 'completed')
	ordering = ('-datetime')

admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(InventoryOrder, InventoryOrderAdmin)
admin.site.register(ItemSold, ItemSoldAdmin)