import cv2
from django.conf import settings

from apps.modelos.models import MamografiaUploadFile

from core.settings.develop import MEDIA_URL, BASE_DIR
from apps.modelos.apps import (
    model_loaded_signal,
)  # Importa la señal personalizada desde tu aplicación


class MamografiaAppService(object):
    @staticmethod
    def pre_procesar_datos():
        MamografiaUploadFile.objects.all().delete()

    @staticmethod
    def procesar_datos(mamografia_upload):
        horizontal = f"{settings.MEDIA_ROOT}/{mamografia_upload.imagen_horizontal.name}"
        vertical = f"{settings.MEDIA_ROOT}/{mamografia_upload.imagen_vertical.name}"

        return predecir(horizontal, vertical)


def predecir(horizontal, vertical):
    try:
        loaded_model = settings.GLOBAL_LOADED_MODEL

        images = []
        predictions = []

        images.append(
            cv2.resize(cv2.imread(horizontal), (224, 224), interpolation=cv2.INTER_AREA)
        )
        images.append(
            cv2.resize(cv2.imread(vertical), (224, 224), interpolation=cv2.INTER_AREA)
        )

        for i in images:
            predictions.append(float(loaded_model.predict(i[(None, ...)])))

        print(predictions)
        
        return predictions

    except Exception as error:
        print("ERROR", error)
