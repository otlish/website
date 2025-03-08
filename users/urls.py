from .views import RegisterView,LoginView,khalti
from django.urls import path

urlpatterns = [
     path('register/',RegisterView.as_view(),name="Register"),
     path('login/',LoginView.as_view(),name="Login"),
     path('khalti/',khalti,name="Payment"),
 ]
 