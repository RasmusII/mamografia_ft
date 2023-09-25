from django.apps import AppConfig
from django.db.models.signals import ModelSignal

# Define una señal personalizada
model_loaded_signal = ModelSignal()

# Función para cargar el modelo
def load_custom_model():
    from django.conf import settings
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    from core.settings.develop import MEDIA_URL, BASE_DIR

    # Ruta al modelo previamente entrenado
    MODEL_PATH = f"{BASE_DIR}{MEDIA_URL}modelo/modelo_deteccion_Cancer_mama_densenet_final.h5"

    # Carga el modelo
    loaded_model = load_model(MODEL_PATH)
    loaded_model.compile(
            optimizer=tf.keras.optimizers.Adam(1e-4),
            loss=tf.keras.losses.BinaryCrossentropy(),
            metrics=["accuracy"],
    )   

    settings.GLOBAL_LOADED_MODEL = loaded_model

    # Emite la señal personalizada
    model_loaded_signal.send(sender=None, model=loaded_model)
    

class ModelosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.modelos'

    # Sobrescribe el método ready() para cargar el modelo al iniciar la aplicación
    def ready(self):
        super().ready()
        load_custom_model()