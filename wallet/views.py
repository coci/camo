import datetime as dt

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Wallet, RequestType


class SubmitIncome(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		amount = None if not request.POST.get('amount') else request.POST.get('amount')
		description = None if not request.POST.get('description') else request.POST.get('description')
		date = None if not request.POST.get('date') else request.POST.get('date')

		# check amount is not empty
		if not amount:
			content = {
				'status': 'error',
				'detail': {
					'message': 'Amount cannot be empty .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		# check date is not empty
		if not date:
			date = str(dt.datetime.now().date())  # if date is empty its set to today

		# validate date value
		try:
			dt.datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d')
		except ValueError:
			content = {
				'status': 'error',
				'detail': {
					'message': 'Date must be in format : yyyy-mm-dd'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		# check description is not empty
		if not description:
			description = 'income'  # set default to description

		# validate amount
		try:
			amount = int(amount)  # convert amount from str to int
		except ValueError:
			content = {
				'status': 'error',
				'detail': {
					'message': 'Amount must be integer not string .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		# create object
		create_expense = Wallet(
			user=request.user,
			amount=amount,
			date=date,
			description=description,
			type=RequestType.income.value,
		)

		create_expense.save()

		content = {
			'status': 'success',
			'result': {
				'user': f'{create_expense.user.username}',
				'type': f'{create_expense.type}',
				'amount': f'{create_expense.amount}',
				'description': f'{create_expense.description}',
			}
		}
		return Response(content, status=status.HTTP_201_CREATED)


class SubmitExpense(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		amount = None if not request.POST.get('amount') else request.POST.get('amount')
		description = None if not request.POST.get('description') else request.POST.get('description')
		date = None if not request.POST.get('date') else request.POST.get('date')

		# check amount is not empty
		if not amount:
			content = {
				'status': 'error',
				'detail': {
					'message': 'Amount cannot be empty .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		# check date is not empty
		if not date:
			date = str(dt.datetime.now().date())  # if date is empty its set to today

		# validate date value
		try:
			dt.datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d')
		except ValueError:
			content = {
				'status': 'error',
				'detail': {
					'message': 'Date must be in format : yyyy-mm-dd'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		# check description is not empty
		if not description:
			description = 'expense'  # set default to description

		# validate amount
		try:
			amount = int(amount)  # convert amount from str to int
		except ValueError:
			content = {
				'status': 'error',
				'detail': {
					'message': 'Amount must be integer not string .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		# create object
		create_expense = Wallet(
			user=request.user,
			amount=amount,
			date=date,
			description=description,
			type=RequestType.expense.value,
		)

		create_expense.save()

		content = {
			'status': 'success',
			'result': {
				'user': f'{create_expense.user.username}',
				'type': f'{create_expense.type}',
				'amount': f'{create_expense.amount}',
				'description': f'{create_expense.description}',
			}
		}
		return Response(content, status=status.HTTP_201_CREATED)
