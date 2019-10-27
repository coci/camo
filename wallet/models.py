from django.db import models
from enum import Enum

# Create your models here.
from camo import settings


class ExpenseCategory(Enum):
	food = 'خوراک'
	cloth = 'پوشاک'
	transportation = 'حمل و نقل'
	entertainment = 'تفریح'
	other = 'متفرقه'


class IncomeCategory(Enum):
	salary = 'حقوق'
	other = 'متفرقه'


def factor(instance, filename):
	"""
	this will create directory for each user to store image init
	"""
	return '/'.join(['factor', str(instance.pk), filename])


class Income(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	amount = models.IntegerField()
	description = models.TextField()
	date = models.DateField()
	category = models.CharField(
		max_length=100,
		choices=[(IncomeCategory.name, IncomeCategory.value) for IncomeCategory in IncomeCategory],
		null=True,
		blank=True
	)

	def __str__(self):
		return f'{self.user} has income with this amount : {self.amount}'


class Expense(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	amount = models.IntegerField()
	description = models.TextField()
	date = models.DateField()
	category = models.CharField(
		max_length=100,
		choices=[(ExpenseCategory.name, ExpenseCategory.value) for ExpenseCategory in ExpenseCategory],
		null=True,
		blank=True
	)

	def __str__(self):
		return f'{self.user} has expense with this amount : {self.amount}'
