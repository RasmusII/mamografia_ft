from django.contrib import admin
from .models import Paciente, Mamografia, MamografiaImage, MamografiaUploadFile, CustomUser

# Register your models here.

class MamografiaImageInLine(admin.TabularInline):
    model = MamografiaImage
    extra = 2


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'password')

class PacienteAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'cedula', 'apellido_paterno',
                    'apellido_materno', 'nombre', 'createdAt', 'updatedAt')


class MamografiaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'external_id', 'paciente', 'resultado',
                    'descripcion', 'createdAt', 'updatedAt')
    inlines = [MamografiaImageInLine]


class MamografiaImageAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'mamografia', 'createdAt', 'updatedAt')


class MamografiaUploadField(admin.ModelAdmin):
    list_display = ('pk', 'paciente', 'lado_mamario')

admin.site.register(Paciente, PacienteAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Mamografia, MamografiaAdmin)
admin.site.register(MamografiaImage, MamografiaImageAdmin)
admin.site.register(MamografiaUploadFile, MamografiaUploadField)

