# Importación Librerias Django
from django.http import JsonResponse
from django.shortcuts import render
from core.settings.develop import MEDIA_URL, STATIC_URL, BASE_DIR
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from apps.modelos.models import Mamografia, MamografiaImage, MamografiaUploadFile
from apps.modelos.forms import *

# Importacion Tensorflow
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array


import os


# Create your views here.


def home(self):
    model = f'{BASE_DIR}{MEDIA_URL}modelo_deteccion_Cancer_mama_vgg16.h5'
    # Cancer: 0
    # Normal: 1

    modelo = load_model(model)
    modelo.compile(
        optimizer=tf.keras.optimizers.Adagrad(1.0e-4),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=['accuracy']
    )
    if not modelo:
        print('Error carga de Modelo')

    image = tf.keras.utils.load_img(
        'D:\DATASET CANCER MAMA\DATASET CANCER/archive\MINI-DDSM-Complete-JPEG-8/train\Maligno\A_1329_1.LEFT_CC.jpg', target_size=(255, 255))
    image_array = img_to_array(image)

    prediction = modelo.predict(image_array[(None, ...)])

    print(prediction)

    return JsonResponse({'Modelo_path': model})



class MamografiaListView(ListView):
    model = Mamografia
    template_name = 'mamografia/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mamografias'
        context['entity'] = 'Mamografia'
        context['mamografia'] = Mamografia.objects.filter(paciente__external_id=self.kwargs.get('external'))
        context['create_url'] = reverse_lazy('core:mamografia_create', args=[self.kwargs.get('external')])
        context['list_url'] = reverse_lazy('core:mamografia_list', args=[self.kwargs.get('external')])
        return context

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Mamografia.objects.filter(paciente__external_id=kwargs.get('external')):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    

class MamografiaUploadView(CreateView):
    model = MamografiaUploadFile
    form_class = MamografiaUploadForm
    template_name = 'mamografia/create.html'
    success_url = reverse_lazy('core:pacientes_list')
    
    def get_context_data(self, **kwargs):
        context = super(MamografiaUploadView, self).get_context_data(**kwargs)
        context['title'] = 'Registro de Mamografias'
        context['entity'] = 'Mamografias'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['paciente'] = Paciente.objects.get(external_id=self.kwargs.get('external'))
        if "form" not in context:
            context['form'] = self.form_class(self.request.GET, external=12121)
        return context
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class MamografiaCreate(CreateView):
    model = Mamografia
    second_model = MamografiaImage
    form_class = MamografiaForm
    second_form_class = MamografiaImageForm
    third_form_class = MamografiaImageForm
    template_name = 'mamografia/create.html'
    success_url = reverse_lazy('core:pacientes_list')
    
    def get_context_data(self, **kwargs):
        context = super(MamografiaCreate, self).get_context_data(**kwargs)
        context['title'] = 'Registro de Mamografias'
        context['entity'] = 'Mamografias'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['paciente'] = Paciente.objects.get(external_id=self.kwargs.get('external'))
        if "form" not in context:
            context['form'] = self.form_class(self.request.GET)
        if "form2" not in context:
            context['form_image_left'] = self.second_form_class(
                self.request.GET)
        if "form3" not in context:
            context['form_image_right'] = self.third_form_class(
                self.request.GET)
        # context['form_image_right'] = MamografiaImageForm()
        return context


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            form = self.form_class(request.POST)
            paciente = Paciente.objects.get(external_id=self.kwargs.get('external'))
            if action == 'add' and form.is_valid():
                # procesar modelo
                mamografia = Mamografia()
                mamografia.resultado = request.POST['resultado']
                mamografia.orientacion = 0
                mamografia.descripcion = request.POST['descripcion']
                mamografia.paciente = paciente
                mamografia.save()
                MamografiaImage.objects.create(imagen=request.FILES.getlist('imagen')[0], orientacion=0, mamografia=mamografia),
                MamografiaImage.objects.create(imagen=request.FILES.getlist('imagen')[1], orientacion=1, mamografia=mamografia)
                data = mamografia
                return redirect(self.success_url)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)



class MamografiaInline():
    model = Mamografia
    form_class = MamografiaForm
    template_name = 'mamografia/create2.html'
    success_url = reverse_lazy('core:pacientes_list')

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        self.object = form.save()
        for name, formset in named_formsets.items():
            formset_save_func = getattr(
                self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect(self.success_url)

    def formset_catalog_item_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        catalog_item = formset.save(
            commit=False)  # self.save_formset(formset, contact)
        for obj in formset.deleted_objects:
            obj.delete()
        for item in catalog_item:
            item.catalog = self.object
            item.save()


class MamografiaCreatess(MamografiaInline, CreateView):

    def get_context_data(self, **kwargs):
        context = super(MamografiaCreatess, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        context['entity'] = 'Categoria'
        context['second_entity'] = 'Item Categoria'
        context['action'] = 'add'
        return context

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'catalog_item': MamografiaImageFormSet(prefix='catalog_item')
            }
        else:
            return {
                'catalog_item': MamografiaImageFormSet(
                    self.request.POST or None, self.request.FILES or None, prefix='catalog_item'
                )
            }
            