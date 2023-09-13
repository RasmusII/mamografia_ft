from datetime import datetime
from django.conf import settings
from apps.modelos.models import (
    Paciente,
    MamografiaUploadFile,
    Mamografia,
    MamografiaImage,
)
import os
import cv2

# Importacion Tensorflow
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

from core.settings.develop import MEDIA_URL, BASE_DIR


class MamografiaAppService(object):
    @staticmethod
    def pre_procesar_datos():
        MamografiaUploadFile.objects.all().delete()

    @staticmethod
    def procesar_datos(mamografia_upload):
        horizontal = f"{settings.MEDIA_ROOT}/{mamografia_upload.imagen_horizontal.name}"
        vertical = f"{settings.MEDIA_ROOT}/{mamografia_upload.imagen_vertical.name}"
        predecir(horizontal, vertical, mamografia_upload)


def predecir(horizontal, vertical, object):
    try:
        model = f"{BASE_DIR}{MEDIA_URL}modelo/modelo_deteccion_Cancer_mama_densenet_final.h5"
        modelo = load_model(model)
        modelo.compile(
            optimizer=tf.keras.optimizers.Adam(1e-4),
            loss=tf.keras.losses.BinaryCrossentropy(),
            metrics=["accuracy"],
        )

        images = []
        predictions = []

        images.append(
            cv2.resize(cv2.imread(horizontal), (224, 224), interpolation=cv2.INTER_AREA)
        )
        images.append(
            cv2.resize(cv2.imread(vertical), (224, 224), interpolation=cv2.INTER_AREA)
        )

        for i in images:
            predictions.append(float(modelo.predict(i[(None, ...)])))

        print("preccin ", predictions)
        if predictions[0] > 0.5 or predictions[1] > 0.5:
            return Mamografia.objects.create(
                orientacion=object.lado_mamario,
                resultado=1,
                descripcion="Cancer",
                paciente=Paciente.objects.get(external_id=object.paciente),
            )

        return Mamografia.objects.create(
            orientacion=object.lado_mamario,
            resultado=0,
            descripcion="Sin Cancer",
            paciente=Paciente.objects.get(external_id=object.paciente),
        )

    except Exception as e:
        print("ERROR %s" % e)
        print("error ctm")
