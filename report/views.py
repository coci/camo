import datetime as dt

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from date.date import jalali_to_gregorian, gregorian_to_jalali
from wallet.models import Income, Expense
import datetime
from django.db.models import Q
from .serializers import IncomeSerializer


class IncomeReport(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		from_date = request.POST.get('from_date') if request.POST.get('from_date') else None
		to_date = request.POST.get('to_date') if request.POST.get('to_date') else None

		if not from_date:
			from_date = datetime.datetime.now()
		else:
			try:
				date = jalali_to_gregorian(from_date)
			except ValueError:
				content = {
					'status': 'error',
					'detail': {
						'message': 'Date must be in format : yyyy-mm-dd'
					}
				}
				return Response(content, status=status.HTTP_400_BAD_REQUEST)

		if not to_date:
			to_date = datetime.datetime.now()
		else:
			try:
				date = jalali_to_gregorian(to_date)
			except ValueError:
				content = {
					'status': 'error',
					'detail': {
						'message': 'Date must be in format : yyyy-mm-dd'
					}
				}
				return Response(content, status=status.HTTP_400_BAD_REQUEST)

		income = Income.objects.filter(user=request.user)
		income = income.filter(
			Q(date__range=(from_date, to_date))
		)

		income = IncomeSerializer(income, many=True)

		counter = 0
		for i in income.data:
			income.data[counter]['date'] = gregorian_to_jalali(i['date'])
			counter += 1

		return Response(income.data, status=status.HTTP_200_OK)
