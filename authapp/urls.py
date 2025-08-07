from django.urls import path
from .views import login_start, login_callback, logout_view
urlpatterns=[
    path("login", login_start, name="auth-login"),
    path("callback", login_callback, name="auth-callback"),
    path("logout", logout_view, name="auth-logout"),
]
