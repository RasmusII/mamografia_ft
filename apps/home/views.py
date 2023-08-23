from django.views.generic import TemplateView
# Create your views here.

class Home(TemplateView):
    template_name = 'homepage/index.html'