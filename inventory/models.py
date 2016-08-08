
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

class FactoryContract(models.Model):
	class Meta:
		ordering = ['-date_created']

	contract_number = models.CharField(max_length=32)
	manager = models.ForeignKey(User)
	factory = models.CharField(max_length=255, choices=FACTORY, null=True, blank=True)
	total_price = models.DecimalField(max_digits=10, decimal_places=2)
	date_created = models.DateTimeField(auto_now_add=True)
	notes = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.contract_number

	def is_all_item_delivered(self):
		f_list = FactoryOrderItem.objects.filter(contract=self)
		if f_list.count() == 0:
			return False
		for l in f_list:
			if not l.is_complete():
				return False
		return True
	is_all_item_delivered.boolean = True

class FactoryOrderItem(models.Model):
	class Meta:
		ordering = ['-date_created']

	contract = models.ForeignKey(FactoryContract)
	item = models.ForeignKey(Product)
	order_quantity = models.IntegerField()
	date_created = models.DateTimeField(auto_now_add=True)
	factory = models.CharField(max_length=255, choices=FACTORY, null=True, blank=True)
	number_received = models.IntegerField(default=0)

	def expecting(self):
		return self.order_quantity - self.number_received

	def is_complete(self):
		return self.order_quantity == self.number_received
	is_complete.boolean = True


class ClientContract(models.Model):
	class Meta:
		ordering = ['-date_created']

	contract_number = models.CharField(max_length=32)
	manager = models.ForeignKey(User)
	client_name = models.CharField(max_length=32)
	total_price = models.DecimalField(max_digits=10, decimal_places=2)
	date_created = models.DateTimeField(auto_now_add=True)
	notes = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.contract_number

	def is_all_item_installed(self):
		c_list = ClientOrderItem.objects.filter(contract=self)
		if c_list.count() == 0:
			return False
		for l in c_list:
			if not l.is_complete():
				return False
		return True
	is_all_item_installed.boolean = True

class ClientOrderItem(models.Model):
	class Meta:
		ordering = ['-date_created']

	contract = models.ForeignKey(ClientContract)
	item = models.ForeignKey(Product)
	order_quantity = models.IntegerField()
	date_created = models.DateTimeField(auto_now_add=True)
	number_installed = models.IntegerField(default=0)

	def ongoing(self):
		return self.order_quantity - self.number_installed

	def is_complete(self):
		return self.order_quantity == self.number_installed
	is_complete.boolean = True

class Inventory(models.Model):

	product = models.ForeignKey(Product)
	start_off_quantity = models.IntegerField()

	def product_model(self):
		return self.product.model

	def current_quantity(self):
		in_list = FactoryOrderItem.objects.filter(item=self.product)
		out_list = ClientOrderItem.objects.filter(item=self.product)
		in_quantity = 0
		out_quantity = 0

		for l in in_list:
			in_quantity += l.number_received
		for l in out_list:
			out_quantity += l.number_installed

		return self.start_off_quantity + in_quantity - out_quantity

	def factory_onhold_item(self):
		in_list = FactoryOrderItem.objects.filter(item=self.product)
		in_quantity = 0
		for l in in_list:
			in_quantity += l.order_quantity - l.number_received
		return in_quantity

	def client_onhold_item(self):
		out_list = ClientOrderItem.objects.filter(item=self.product)
		out_quantity = 0
		for l in out_list:
			out_quantity += l.order_quantity - l.number_installed

		return out_quantity

	def resulting_quantity(self):
		in_list = FactoryOrderItem.objects.filter(item=self.product)
		out_list = ClientOrderItem.objects.filter(item=self.product)
		in_quantity = 0
		out_quantity = 0

		for l in in_list:
			in_quantity += l.order_quantity
		for l in out_list:
			out_quantity += l.order_quantity
		return self.start_off_quantity + in_quantity - out_quantity

	def quantity_status(self):
		if self.resulting_quantity() >= 0:
			return True
		else:
			return False
	quantity_status.boolean = True

