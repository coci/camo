from django.urls import path
from .views import SubmitIncome, SubmitExpense

urlpatterns = [
	path('income/', SubmitIncome.as_view(), name='submit_income'),
	path('expense/', SubmitExpense.as_view(), name='submit_expense'),
]
