from django.urls import path
from . import views

# app_name = 'users'

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    # path("login/", views.index, name="login")
]
