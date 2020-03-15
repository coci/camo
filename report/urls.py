from django.urls import path
from .views import IncomeList

urlpatterns = [
	path('income/', IncomeList.as_view())
]
