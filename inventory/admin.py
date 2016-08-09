from django.contrib import admin
from django import forms
from inventory.models import *
from inventory.constants import *

class InventoryAdmin(admin.ModelAdmin):
	list_display = ('product', 'current_quantity', 'factory_onhold_item', 'client_onhold_item', 'resulting_quantity', 'quantity_status')
	ordering = ['product']
	search_fields = ['^product__model']

class ProductAdmin(admin.ModelAdmin):
	list_display = ('model', 'color', 'suggested_price', 'cost')
	ordering = ['model', 'color']

class FactoryAdmin(admin.ModelAdmin):
	list_display = ['name']
	ordering = ['name']

class FactoryOrderItemInline(admin.TabularInline):
	model = FactoryOrderItem
	extra = 5

class FactoryContractAdmin(admin.ModelAdmin):
	list_display = ('contract_number', 'manager', 'factory', 'date_created', 'total_price', 'is_all_item_delivered')
	ordering = ['-date_created']
	search_fields = ['^contract_number']
	inlines = [FactoryOrderItemInline]

class FactoryOrderItemAdmin(admin.ModelAdmin):
	list_display = ('contract', 'item', 'order_quantity', 'date_created', 'number_received', 'expecting', 'is_complete')
	ordering = ['-date_created']
	search_fields = ['^item__model']

class ClientOrderItemInline(admin.TabularInline):
	model = ClientOrderItem
	extra = 5

class ClientContractAdmin(admin.ModelAdmin):
	list_display = ('contract_number', 'manager', 'client_name', 'date_created', 'total_price', 'is_all_item_installed')
	ordering = ['-date_created']
	search_fields = ['contract__client_name']
	inlines = [ClientOrderItemInline]

class ClientOrderItemAdmin(admin.ModelAdmin):
	list_display = ('contract', 'item', 'order_quantity', 'date_created', 'number_installed', 'ongoing', 'is_complete')
	ordering = ['-date_created']
	search_fields = ['contract__client_name']

admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Factory, FactoryAdmin)
admin.site.register(FactoryContract, FactoryContractAdmin)
admin.site.register(FactoryOrderItem, FactoryOrderItemAdmin)
admin.site.register(ClientContract, ClientContractAdmin)
admin.site.register(ClientOrderItem, ClientOrderItemAdmin)