from django.db import models
from enum import Enum

# Create your models here.
from camo import settings


class RequestType(Enum):
	expense = 'expense'
	income = 'income'


class Wallet(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	amount = models.IntegerField()
	description = models.TextField()
	date = models.DateField()
	type = models.CharField(max_length=100,
							choices=[(RequestType.name, RequestType.value) for RequestType in RequestType])

	def __str__(self):
		return f'{self.user} has {self.type} with this amount : {self.amount}'
