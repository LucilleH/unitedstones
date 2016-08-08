
import os

from django.contrib.auth.models import User
from django.db import models
from django import forms
from inventory.constants import COLOR, FACTORY, ORDERSTATUS

class Product(models.Model):
	class Meta:
		ordering = ['model']

	name = models.CharField(max_length=100)
	model = models.CharField(max_length=20)
	color = models.IntegerField(choices=COLOR, null=False, blank=False)
	suggested_price = models.DecimalField(max_digits=10, decimal_places=2)
	cost = models.DecimalField(max_digits=10, decimal_places=2)
	description = models.TextField(null=True, blank=True)
	picture_name = models.CharField(max_length=255, null=True, blank=True)
	
	def __unicode__(self):
		return self.model + ' - ' + self.get_color_display()

	def get_name(self):
		return self.name

class InventoryOrder(models.Model):
	class Meta:
		ordering = ['-datetime']

	manager = models.ForeignKey(User)
	item = models.ForeignKey(Product)
	quantity = models.IntegerField()
	datetime = models.DateTimeField(auto_now=True)
	factory = models.CharField(max_length=255, choices=FACTORY, null=True, blank=True)
	arrived = models.BooleanField(default=False)

class ItemSold(models.Model):
	class Meta:
		ordering = ['-datetime']

	user = models.ForeignKey(User)
	item = models.ForeignKey(Product)
	quantity = models.IntegerField()
	datetime = models.DateTimeField(auto_now=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	status = models.IntegerField(choices=ORDERSTATUS, null=True, blank=True)
	completed = models.BooleanField(default=False)

class Inventory(models.Model):

	product = models.ForeignKey(Product)
	start_off_quantity = models.IntegerField()

	def product_model(self):
		return self.product.model

	def current_quantity(self):
		in_list = InventoryOrder.objects.filter(item=self.product, arrived=True)
		out_list = ItemSold.objects.filter(item=self.product, completed=True)
		in_quantity = 0
		out_quantity = 0

		for l in in_list:
			in_quantity += l.quantity
		for l in out_list:
			out_quantity += l.quantity

		return self.start_off_quantity + in_quantity - out_quantity

	def quantity_status(self):
		if self.current_quantity() > 5:
			return True
		else:
			return False
	quantity_status.boolean = True

