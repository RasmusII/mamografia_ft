from django.urls import path

from apps.modelos.views.authentication import LoginView, LogoutView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]