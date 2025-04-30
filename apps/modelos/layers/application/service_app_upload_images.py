import cv2
import numpy as np

from django.conf import settings

from apps.modelos.models import MamografiaUploadFile

from collections import defaultdict
from django.core.files.uploadedfile import UploadedFile

from core.settings.develop import MEDIA_URL, BASE_DIR
from apps.modelos.apps import (
    model_loaded_signal,
)  # Importa la señal personalizada desde tu aplicación
from apps.modelos.models import Mamografia, Paciente, MamografiaImage


class MamografiaAppService(object):
    @staticmethod
    def pre_procesar_datos():
        MamografiaUploadFile.objects.all().delete()

    @staticmethod
    def procesar_datos(mamografia_upload):
        
        vertical = f"{settings.MEDIA_ROOT}/{mamografia_upload.imagen_horizontal.name}"
        horizontal = f"{settings.MEDIA_ROOT}/{mamografia_upload.imagen_vertical.name}"
        
        return predecir(horizontal, vertical)
    
    @staticmethod
    def cargar_mamografias_masivamente(files: list):
        # Estructura: {(dni, lado_mamario): {"MLO": file, "C"C: file}}
        mamografias_agrupadas = defaultdict(dict)

        for file in files:
            filename = file.name
            dni = filename.strip().split("_")[0]
            lado_mamario = 0 if "RIGHT" in filename.upper() else 1

            if "MLO" in filename.upper():
                mamografias_agrupadas[(dni, lado_mamario)]["MLO"] = file
            elif "CC" in filename.upper():
                mamografias_agrupadas[(dni, lado_mamario)]["CC"] = file

        for (dni, lado_mamario), imagenes in mamografias_agrupadas.items():
            horizontal = imagenes.get("MLO")
            vertical = imagenes.get("CC")

            if not horizontal or not vertical:
                print(f"Saltando paciente {dni} - lado {lado_mamario}, falta una imagen.")
                continue  # O puedes registrar un warning

            # Crea el registro en MamografiaUploadFile
            mamografia_upload = MamografiaUploadFile.objects.create(
                paciente=dni,
                imagen_horizontal=horizontal,
                imagen_vertical=vertical,
                lado_mamario=lado_mamario
            )

            # Procesamiento del modelo
            resultado = MamografiaAppService.procesar_datos(mamografia_upload)
            # Obtener el paciente y crear el registro principal
            paciente = Paciente.objects.filter(cedula__iexact=dni)
            if paciente.exists():
                mamografia = Mamografia.objects.create(
                    paciente=paciente.first(),
                    lado_mamario=lado_mamario,
                    resultado=max(resultado)
                )

                # Crear imágenes asociadas
                MamografiaImage.objects.create(
                    imagen=mamografia_upload.imagen_horizontal.url.replace("/media", ""),
                    orientacion=1,
                    mamografia=mamografia,
                    paciente=dni
                )
                MamografiaImage.objects.create(
                    imagen=mamografia_upload.imagen_vertical.url.replace("/media", ""),
                    orientacion=0,
                    mamografia=mamografia,
                    paciente=dni
                )



def predecir(horizontal, vertical):
    try:
        # Modelo previamente cargado desde settings
        loaded_model = settings.GLOBAL_LOADED_MODEL

        # Leer y redimensionar imágenes
        images = [
            cv2.resize(cv2.imread(horizontal), (224, 224), interpolation=cv2.INTER_AREA),
            cv2.resize(cv2.imread(vertical), (224, 224), interpolation=cv2.INTER_AREA)
        ]

        predictions = []

        for img in images:
            # Expandir dimensiones para formar un batch de 1
            img_batch = np.expand_dims(img, axis=0)

            # Realizar predicción (devuelve probabilidades por clase)
            pred = loaded_model.predict(img_batch)

            # Obtener la clase con mayor probabilidad
            print("Predicciones:", pred)
            pred_label = np.argmax(pred, axis=1)[0]
            predictions.append(pred_label)

        print("Predicciones del modelo:", predictions)

        return predictions
    
    except Exception as error:
        print("ERROR", error)
