from django.urls import path
from .views import UserRegisteration

urlpatterns = [
	path("register", UserRegisteration.as_view(), name="hello")
]
