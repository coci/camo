import datetime as dt

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from wallet.models import Wallet, RequestType


class IncomeReport(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		duration = None if not request.POST.get('duration') else request.POST.get('duration')

