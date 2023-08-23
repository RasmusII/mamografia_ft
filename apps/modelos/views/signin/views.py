from django.contrib.auth.decorators import login_required
from django.forms.models import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt  
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, FormView

from core.settings.develop import BASE_DIR, MEDIA_URL, STATIC_URL
from apps.modelos.forms import *  # Importar solo los formularios necesarios o especificar cada formulario por separado
from apps.modelos.models import *  # Importar solo los modelos necesarios o especificar cada modelo por separado

# Sign Up View
class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    success_url = reverse_lazy('core:login')
    template_name = 'registration/register.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form = self.form_class(self.request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.set_password(form.cleaned_data['password'])
            data.save()
            
        return super().form_valid(form)

    
