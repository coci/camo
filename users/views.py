from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import CustomUser


class UserRegisteration(APIView):
	"""
	use this for register user on system

	this class doesn't need any authorization method ( token in header ) .

	:methods:
				[post] -> [url] : www.domain.com/api/v1/user/register
					:body:
						- username :
							type : string
							required : true
							description : username must be 6 character or more
						- password :
							type : string
							required : true
							description : password must be 6 character or more
						- first_name :
							type : string
							required : true
						- last_name :
							type : string
							required : true

					:return
						-username
						-fullname
						-token

				[get] :
						None
	"""
	permission_classes = ()

	def post(self, request):
		username = None if not request.POST.get('username') else request.POST.get('username')
		password = None if not request.POST.get('password') else request.POST.get('password')
		last_name = None if not request.POST.get('last_name') else request.POST.get('last_name')
		first_name = None if not request.POST.get('first_name') else request.POST.get('first_name')

		if not username:  # check username not be empty
			content = {
				'status': 'error',
				'detail': {
					'message': 'Username cannot be empty .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		if len(username) < 5:  # check username more than 5 character
			content = {
				'status': 'error',
				'detail': {
					'message': 'Username must be 6 character or more .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		if CustomUser.objects.filter(username=username).exists():  # check username doesn't exist in db
			content = {
				'status': 'error',
				'detail': {
					'message': 'Username already exist .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		if not password:  # check password not be empty
			content = {
				'status': 'error',
				'detail': {
					'message': 'Password cannot be empty .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		if len(password) < 6:  # check password username more than 5 character
			content = {
				'status': 'error',
				'detail': {
					'message': 'Password must be 6 character or more .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		if not first_name or not last_name:  # check first_name and last_name not be empty
			content = {
				'status': 'error',
				'detail': {
					'message': 'Last name and first name cannot be empty .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		try:  # try to create user
			create_user = CustomUser(username=username, last_name=last_name, first_name=first_name)
			create_user.set_password(password)
			create_user.save()

			token = Token.objects.get(user=create_user)  # get user token

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
					'message': 'Something wrong , please try again .'
				}
			}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)
		return Response(content, status=status.HTTP_201_CREATED)
