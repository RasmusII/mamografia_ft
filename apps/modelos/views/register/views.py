from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt  
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, FormView

from core.settings.develop import BASE_DIR, MEDIA_URL, STATIC_URL
from apps.modelos.forms import *  # Importar solo los formularios necesarios o especificar cada formulario por separado
from apps.modelos.models import *  # Importar solo los modelos necesarios o especificar cada modelo por separado

class CreateView(CreateView):
    model = Mamografia
    template_name = 'mamografia/create.html'
    fields = '__all__'
    success_url = reverse_lazy('mamografia_list')
