from django.urls import path

from apps.modelos.views.paciente.views import (
   PacienteListView, PacienteCreateView,
   PacienteUpdateView,
)

urlpatterns = [
   # path('modelo/', home, name='home'),
   # Pacientes
   path("pacientes/", PacienteListView.as_view(), name="pacientes_list"),
   path("paciente/", PacienteCreateView.as_view(), name="pacientes_create"),
   path("paciente/<int:pk>/", PacienteUpdateView.as_view(), name="pacientes_create"),
]
