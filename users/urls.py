from django.urls import path
from .views import UserRegisteration
from rest_framework.authtoken import views


urlpatterns = [
	path("register", UserRegisteration.as_view(), name="register"),
	path('token/', views.obtain_auth_token),
]
