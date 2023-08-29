from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.modelos.forms import *  # Importar solo los formularios necesarios o especificar cada formulario por separado
from apps.modelos.models import *  # Importar solo los modelos necesarios o especificar cada modelo por separado
from django.views.decorators.csrf import csrf_exempt  



class LoginView(LoginView):
    model = Mamografia
    fields = '__all__'
    template_name = 'registration/login.html'
    success_url = reverse_lazy('core:pacientes_list')

    @csrf_exempt  # Añadir protección CSRF a la vista
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return self.success_url
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))






