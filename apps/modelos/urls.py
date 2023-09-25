from django.urls import path

from apps.modelos.views.paciente.views import (
   PacienteListView, PacienteCreateView,
   PacienteUpdateView,
)

from apps.modelos.views.mamografia.views import (
   MamografiaUploadView, MamografiaListView,
   MamografiaCreate, MamografiaUpdateView
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
   path('mamografia/predict/<str:external>/', MamografiaUploadView.as_view(), name='mamografia_predict'),
   path('mamografia/create/<int:result>/<int:mamografia>/', MamografiaCreate.as_view(), name='mamografia_create'),
   path('mamografia/edit/<int:pk>/', MamografiaUpdateView.as_view(), name='mamografia_create'),
   
   
   
]
