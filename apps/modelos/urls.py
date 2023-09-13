from django.urls import path

from .views.login.views import LoginView
from .views.signin.views import SignUpView
from django.contrib.auth.views import LogoutView
from apps.modelos.views.paciente.views import (
   PacienteListView,
   PacienteCreateView,
   PacienteUpdateView,
)

from apps.modelos.views.mamografia.views import (
   MamografiaUploadView, MamografiaListView
)

app_name = "core"

urlpatterns = [
   # path('modelo/', home, name='home'),
   # Pacientes
   path("pacientes/", PacienteListView.as_view(), name="pacientes_list"),
   path("paciente/", PacienteCreateView.as_view(), name="pacientes_create"),
   path("paciente/<int:pk>/", PacienteUpdateView.as_view(), name="pacientes_create"),

   # Mamografia
   path('mamografia/<str:external>/', MamografiaListView.as_view(), name='mamografia_list'),
   path('mamografia/create/<str:external>/', MamografiaUploadView.as_view(), name='mamografia_create'),
   
   
   # LISTAR MAMOGRAFIA
   #  path('login/', LoginView.as_view(), name='login'),
   #  path('logout/', LogoutView.as_view(next_page='core:login'),name='logout'),
   #  path('signup/', SignUpView.as_view(), name='signup'),
]
