# from django.contrib.auth.views import LoginView
# from django.urls import reverse_lazy
# from django.contrib import messages
# from apps.modelos.forms import *  # Importar solo los formularios necesarios o especificar cada formulario por separado
# from apps.modelos.models import *  # Importar solo los modelos necesarios o especificar cada modelo por separado
# from django.views.decorators.csrf import csrf_exempt  


# class LoginView(LoginView):
#     model = Mamografia
#     fields = '__all__'
#     template_name = 'registration/login.html'
#     success_url = reverse_lazy('core:pacientes_list')

#     def get_success_url(self):
#         return self.success_url
    
#     def form_invalid(self, form):
#         messages.error(self.request, 'Invalid username or password')
#         return self.render_to_response(self.get_context_data(form=form))

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from apps.modelos.forms import SignInForm
from apps.modelos.layers.application.user_app_service import UserAppService
from apps.modelos.models import CustomUser


class LoginView(LoginView):
    model = CustomUser
    form_class = SignInForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("core:pacientes_list")
    success_message = "Login successful"

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        identifier = request.POST.get("username")
        password = request.POST.get("password")

        user = UserAppService.get_user_by_identifier(identifier)

        if not user:
            messages.warning(self.request, "Invalid username or password")

        # Se pasa el nombre de usuario (user.username) en lugar del objeto user
        if self.authenticate_and_login(user, password):
            return self.handle_login_success(user)

        messages.warning(request, "Invalid username or password")
        return render(request, self.template_name, {"form": form})

    def authenticate_and_login(self, username, password):
        """Attempts to authenticate and log in the user."""
        access = authenticate(username=username, password=password)
        if access:
            login(self.request, access)
            return True
        return False

    def handle_login_success(self, user):
        """Handles post-login actions and redirects."""
        messages.success(self.request, self.success_message)
        next_url = self.request.GET.get("next", self.success_url)
        return redirect(next_url)


class SignOutView(LogoutView):
    http_method_names = ["post"]
    next_page = "login"

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.next_page)




