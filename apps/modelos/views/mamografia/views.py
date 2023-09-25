from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView
from apps.modelos.models import Mamografia, MamografiaImage, MamografiaUploadFile
from apps.modelos.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.modelos.layers.application.service_app_upload_images import MamografiaAppService



class MamografiaListView(LoginRequiredMixin, ListView):
    model = Mamografia
    template_name = "mamografia/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Mamografias"
        context["entity"] = "Mamografia"
        context["mamografia"] = Mamografia.objects.filter(
            paciente__external_id=self.kwargs.get("external")
        )
        context["create_url"] = reverse_lazy(
            "core:mamografia_predict", args=[self.kwargs.get("external")]
        )
        context["list_url"] = reverse_lazy(
            "core:mamografia_list", args=[self.kwargs.get("external")]
        )
        return context

    @method_decorator(csrf_exempt, login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in Mamografia.objects.filter(
                    paciente__external_id=kwargs.get("external")
                ):
                    data.append(i.toJSON())
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)


class MamografiaUploadView(LoginRequiredMixin, CreateView):
    model = MamografiaUploadFile
    form_class = MamografiaUploadForm
    template_name = "mamografia/predict.html"

    def get_context_data(self, **kwargs):
        context = super(MamografiaUploadView, self).get_context_data(**kwargs)
        context["title"] = "Registro de Mamografias"
        context["entity"] = "Mamografias"
        context["list_url"] = self.success_url
        context["action"] = "add"
        context["paciente"] = Paciente.objects.get(
            external_id=self.kwargs.get("external")
        )
        if self.form_class not in context:
            context["form"] = MamografiaUploadForm(external=self.kwargs.get("external"))
        return context

    @method_decorator(csrf_exempt, login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            external_id = self.kwargs.get("external")
            mamografia_upload = form.save(commit=False)
            mamografia_upload.paciente = external_id
            mamografia_upload.save()

            # Llama al servicio para procesar la mamografía y obtener el resultado
            resultado = MamografiaAppService.procesar_datos(mamografia_upload)
            return redirect(
                "core:mamografia_create",
                result=(
                    1 if float(resultado[0]) > 0.5 and float(resultado[1]) > 0.5 else 0
                ),
                mamografia=mamografia_upload.id,
            )


class MamografiaCreate(LoginRequiredMixin, CreateView):
    model = Mamografia
    form_class = MamografiaForm
    template_name = "mamografia/create.html"
    success_url = reverse_lazy("core:pacientes_list")

    def get_context_data(self, **kwargs):
        context = super(MamografiaCreate, self).get_context_data(**kwargs)
        context["title"] = "Resultado de Mamografia"
        context["entity"] = "Mamografias"
        context["list_url"] = self.success_url
        context["action"] = "add"
        context["mamografia"] = MamografiaUploadFile.objects.get(
            id=self.kwargs.get("mamografia")
        )
        context["prediction"] = self.kwargs.get("result")
        if "form" not in context:
            context["form"] = self.form_class()
        return context

    def form_valid(self, form):
        mamografia_upload = MamografiaUploadFile.objects.get(
            id=self.kwargs.get("mamografia")
        )
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.paciente = Paciente.objects.get(
                external_id=mamografia_upload.paciente
            )
            form_instance.save()
            MamografiaImage.objects.create(
                imagen=mamografia_upload.imagen_horizontal.url.replace("/media", ""),
                orientacion=1,
                mamografia=form_instance,
            )
            MamografiaImage.objects.create(
                imagen=mamografia_upload.imagen_vertical.url.replace("/media", ""),
                orientacion=0,
                mamografia=form_instance,
            )
            return HttpResponseRedirect(self.success_url)  # Redirige a la URL de éxito

        return super().form_invalid(form)

    @method_decorator(csrf_exempt, login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class MamografiaUpdateView(LoginRequiredMixin, UpdateView):
    model = Mamografia
    form_class = MamografiaForm
    template_name = "mamografia/create.html"
    success_url = reverse_lazy("core:pacientes_list")

    def get_context_data(self, **kwargs):
        context = super(MamografiaUpdateView, self).get_context_data(**kwargs)
        context["title"] = "Resultado de Mamografia"
        context["entity"] = "Mamografias"
        context["list_url"] = self.success_url
        context["action"] = "edit"
        context["mamografia"] = Mamografia.objects.get(id=self.kwargs.get("pk"))
        context["imagen"] = MamografiaImage.objects.filter(
            mamografia__id=self.kwargs.get("pk")
        )
        if "form" not in context:
            context["form"] = self.form_class()
        return context

    def form_valid(self, form):
        mamografia_upload = Mamografia.objects.get(id=self.kwargs.get("pk"))
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.paciente = Paciente.objects.get(
                external_id=mamografia_upload.paciente.external_id
            )
            form_instance.save()
            return HttpResponseRedirect(self.success_url)  # Redirige a la URL de éxito

        return super().form_invalid(form)

    @method_decorator(csrf_exempt, login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
