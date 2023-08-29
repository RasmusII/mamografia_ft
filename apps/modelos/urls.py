from django.urls import path, include

from .views.login.views import LoginView
from .views.signin.views import SignUpView
from .views.mama.views import *

from django.contrib.auth.views import LogoutView

app_name = 'core'

urlpatterns = [
     path('modelo/', home, name='home'),
     path('pacientes/', CatalogListView.as_view(), name='pacientes_list'),
     path('pacientes/create', RegistrarPaciente.as_view(), name='pacientes_create'),
     path('pacientes/edit/<int:pk>/',
          ModificarPaciente.as_view(), name='pacientes_update'),
     # Mamografia

     path('mamografia/create/<str:external>/',
          MamografiaCreate.as_view(), name='mamografia_create'),
     #LISTAR MAMOGRAFIA

     path('login/', LoginView.as_view(), name='login'),
     path('logout/', LogoutView.as_view(next_page='core:login'),name='logout'),

     path('signup/', SignUpView.as_view(), name='signup'),

]
