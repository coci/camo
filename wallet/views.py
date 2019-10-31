import datetime as dt

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Income, IncomeCategory, ExpenseCategory, Expense
from common.date import gregorian_to_jalali, jalali_to_gregorian


class SubmitIncome(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		amount = None if not request.POST.get('amount') else request.POST.get('amount')
		description = None if not request.POST.get('description') else request.POST.get('description')
		date = None if not request.POST.get('date') else request.POST.get('date')
		category = None if not request.POST.get('category') else request.POST.get('category')
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

		else:
			try:
				date = jalali_to_gregorian(date)
			except ValueError:
				content = {
					'status': 'error',
					'detail': {
						'message': 'Date must be in format : yyyy-mm-dd'
					}
				}
				return Response(content, status=status.HTTP_400_BAD_REQUEST)

		date = dt.datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d')

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

		if not category:
			category = IncomeCategory.other.value

		if category in IncomeCategory._value2member_map_:
			category = category
		else:
			category = IncomeCategory.other.value
		# create object
		create_Income = Income(
			user=request.user,
			amount=amount,
			date=date,
			description=description,
			category=category,
		)

		create_Income.save()

		content = {
			'status': 'success',
			'result': {
				'user': f'{create_Income.user.username}',
				'category': f'{create_Income.category}',
				'amount': f'{create_Income.amount}',
				'description': f'{create_Income.description}',
				'date': f'{gregorian_to_jalali(create_Income.date)}'
			}
		}
		return Response(content, status=status.HTTP_201_CREATED)


class SubmitExpense(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		amount = None if not request.POST.get('amount') else request.POST.get('amount')
		description = None if not request.POST.get('description') else request.POST.get('description')
		date = None if not request.POST.get('date') else request.POST.get('date')
		category = None if not request.POST.get('category') else request.POST.get('category')
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

		else:
			try:
				date = jalali_to_gregorian(date)
			except ValueError:
				content = {
					'status': 'error',
					'detail': {
						'message': 'Date must be in format : yyyy-mm-dd'
					}
				}
				return Response(content, status=status.HTTP_400_BAD_REQUEST)

		date = dt.datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d')
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

		if not category:
			category = IncomeCategory.other.value

		if category in ExpenseCategory._value2member_map_:  # check category from request.post in enum category
			category = category
		else:
			category = IncomeCategory.other.value

		# create object
		create_expense = Expense(
			user=request.user,
			amount=amount,
			date=date,
			description=description,
			category=category,
		)

		create_expense.save()

		content = {
			'status': 'success',
			'result': {
				'user': f'{create_expense.user.username}',
				'category': f'{create_expense.category}',
				'amount': f'{create_expense.amount}',
				'description': f'{create_expense.description}',
				'date': f'{gregorian_to_jalali(create_expense.date)}'
			}
		}
		return Response(content, status=status.HTTP_201_CREATED)
