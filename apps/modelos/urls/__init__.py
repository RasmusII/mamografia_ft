from django.urls import include, path

app_name = "core"

urlpatterns = [
    path("", include("apps.modelos.urls.auth")),
    path("core/", include("apps.modelos.urls.pacientes")),
    path("core/", include("apps.modelos.urls.mamografias")),
]