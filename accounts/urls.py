from django.urls import path
from . import views

urlpatterns = [
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path("register/", views.register , name="register"),
    path("login/", views.login_view , name="login"),
    path("logout/", views.lougout_view , name="logout")
]
