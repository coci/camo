from django.urls import path
from .views import SubmitIncome, SubmitExpense

urlpatterns = [
	path('income/', SubmitIncome.as_view()),
	path('expense/', SubmitExpense.as_view()),
]
