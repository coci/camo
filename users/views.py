from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import CustomUser





class UserRegisteration(APIView):
	"""
	user register
	"""
	permission_classes = ()

	def post(self, request):
		username = None if not request.POST.get('username') else request.POST.get('username')
		password = None if not request.POST.get('password') else request.POST.get('password')
		last_name = None if not request.POST.get('last_name') else request.POST.get('last_name')
		first_name = None if not request.POST.get('first_name') else request.POST.get('first_name')

		if not username:
			content = {
				'status': 'error',
				'detail': {
					'message': 'Username cannot be empty .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		if len(username) < 5:
			content = {
				'status': 'error',
				'detail': {
					'message': 'Username must be 6 character or more .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		if CustomUser.objects.filter(username=username).exists():
			content = {
				'status': 'error',
				'detail': {
					'message': 'Username already exist .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		if not password:
			content = {
				'status': 'error',
				'detail': {
					'message': 'Password cannot be empty .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		if len(password) < 6:
			content = {
				'status': 'error',
				'detail': {
					'message': 'Password must be 6 character or more .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)
		if not first_name or not last_name:
			content = {
				'status': 'error',
				'detail': {
					'message': 'Last name and first name cannot be empty .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)
		try:
			create_user = CustomUser(username=username, last_name=last_name, first_name=first_name)
			create_user.set_password(password)
			create_user.save()

			token = Token.objects.get(user=create_user)

			content = {
				'status': 'success',
				'result': {
					'user': {
						'id': f'{create_user.pk}',
						'username': f'{create_user.username}',
						'full name': f'{create_user.first_name}' + ' ' + f'{create_user.last_name}',
						'token': f'{token.key}'
					}
				}
			}
		except ValueError:
			content = {
				'status': 'Error',
				'detail': {
					'message': 'Some field you entered is wrong .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)
		return Response(content, status=status.HTTP_201_CREATED)
