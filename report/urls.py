from django.urls import path
from .views import IncomeReport

urlpatterns = [
	path('income/', IncomeReport.as_view())
]
