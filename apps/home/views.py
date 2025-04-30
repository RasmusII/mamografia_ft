# from django.views.generic import TemplateView
# # Create your views here.

# class Home(TemplateView):
#     template_name = 'homepage/index.html'

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class Home(LoginRequiredMixin, TemplateView):
    template_name = "homepage/index.html"
    success_url = reverse_lazy("core:login")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)