from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from apps.modelos.models import Paciente
from apps.modelos.forms import PacienteForm
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = 'paciente/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Pacientes'
        context['entity'] = 'Pacientes'
        context['create_url'] = reverse_lazy('core:pacientes_create') 
        context['list_url'] =  reverse_lazy('core:pacientes_list')
        return context

    @method_decorator(csrf_exempt, login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Paciente.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class PacienteCreateView(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'paciente/paciente_create_or_update.html'
    success_url = reverse_lazy('core:pacientes_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación una Paciente'
        context['entity'] = 'Paciente'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

    @method_decorator(csrf_exempt, login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            form = self.form_class(request.POST)
            if action == 'add' and form.is_valid():
                form = self.get_form()
                data = form.save()
                return redirect(self.success_url)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    
class PacienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'paciente/paciente_create_or_update.html'
    success_url = reverse_lazy('core:pacientes_list')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición Paciente'
        context['entity'] = 'Paciente'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
