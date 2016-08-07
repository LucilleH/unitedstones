
import os

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django import forms
from inventory.constants import COLOR, FACTORY

class Product(models.Model):
	class Meta:
		ordering = ['model']

	name = models.CharField(max_length=100)
	model = models.CharField(max_length=20)
	color = models.CharField(max_length=64, choices=COLOR, null=False, blank=False)
	suggested_price = models.DecimalField(max_digits=10, decimal_places=2)
	cost = models.DecimalField(max_digits=10, decimal_places=2)
	description = models.TextField(null=True, blank=True)
	picture_name = models.CharField(max_length=255)
	
	def __unicode__(self):
		return self.model

	def get_name(self):
		return self.name

class InventoryOrder(models.Model):
	class Meta:
       ordering = ('-datetime')

    manager = models.ForeignKey(User)
    item = models.ForeignKey(Product)
    quantity = models.IntegerField(max_length=5)
    datetime = models.DateTimeField(default=datetime.now)
    factory = models.CharField(max_length=255, choices=FACTORY, null=True, blank=True)
    arrived = model.BooleanField(default=False)

class ItemSold(models.Model):
	class Meta:
       ordering = ('-datetime')

    user = models.ForeignKey(User)
    item = models.ForeignKey(Product)
    quantity = models.IntegerField(max_length=5)
    datetime = models.DateTimeField(default=datetime.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = model.CharField(max_length=255, choices=ORDERSTATUS, null=True, blank=True)
    completed = model.BooleanField(default=False)

class Inventory(models.Model):

	product = models.ForeignKey(Product)
	quantity = models.IntegerField(max_length=5)

	def product_model(self):
		return self.product.model

	def product_color(self):
		return self.product.color

	def current_quantity(self):
		in_list = InventoryOrder.objects.filter(item=self.product)
		out_list = ItemSold.objects.filter(item=self.product)
		in_quantity = 0
		out_quantity = 0

		for l in in_list:
			in_quantity += l.quantity
		for l in out_list:
			out_quantity += l.quantity

		return self.quantity + in_quantity - out_quantity
