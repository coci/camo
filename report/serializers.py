from rest_framework import serializers
from wallet.models import Income, Expense


class IncomeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Income
		fields = '__all__'
