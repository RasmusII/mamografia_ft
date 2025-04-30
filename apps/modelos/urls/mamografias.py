from django.urls import path

from apps.modelos.views.mamografia.views import (
   MamografiaUploadView, MamografiaListView,
   MamografiaCreate, MamografiaUpdateView, MamografiaBulkCreate
)


urlpatterns = [
   # Mamografia
   path('mamografia/<str:external>/', MamografiaListView.as_view(), name='mamografia_list'),
   path('mamografia/predict/<str:external>/', MamografiaUploadView.as_view(), name='mamografia_predict'),
   path('mamografia/create/<int:result>/<int:mamografia>/', MamografiaCreate.as_view(), name='mamografia_create'),
   path('mamografia/edit/<int:pk>/', MamografiaUpdateView.as_view(), name='mamografia_create'),
   path('mamografia/bulk_update', MamografiaBulkCreate.as_view(), name='mamografia_bulk'),
   
]
