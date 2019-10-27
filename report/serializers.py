from rest_framework import serializers
from wallet.models import Income, Expense
from camo.date import gregorian_to_jalali


class IncomeSerializer(serializers.ModelSerializer):


	class Meta:
		model = Income
		fields = '__all__'
