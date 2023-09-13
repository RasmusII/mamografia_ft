from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.conf import settings
from core.settings.develop import MEDIA_URL, STATIC_URL
from django.forms import model_to_dict
import uuid
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("El email debe ser proporcionado")
        if not username:
            raise ValueError("El nombre de usuario debe ser proporcionado")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Atributo que se utilizará para el inicio de sesión en lugar del campo de nombre de usuario predeterminado
    USERNAME_FIELD = "email"
    # Atributos requeridos al crear un usuario
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    class Meta:
        db_table = "custom_user"
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def __str__(self):
        return self.email


class Paciente(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, null=False)
    cedula = models.CharField(max_length=10, blank=False, null=False, unique=True)
    nombre = models.CharField(max_length=350, blank=False, null=False)
    apellido_paterno = models.CharField(max_length=350, blank=False, null=False)
    apellido_materno = models.CharField(max_length=350, blank=False, null=False)
    createdAt = models.DateField("CreatedAt", auto_now=True, auto_now_add=False)
    updatedAt = models.DateField("UpdatedAt", auto_now=True, auto_now_add=False)

    class Meta:
        db_table = "paciente"
        verbose_name = "paciente"
        verbose_name_plural = "pacientes"
        ordering = ["pk"]

    def toJSON(self):
        item = model_to_dict(self)
        item["external_id"] = self.external_id
        return item

    def apellidos(self):
        return f"{self.apellido_paterno} {self.apellido_materno}"

    def __str__(self):
        return self.apellidos() + " " + self.nombre


class Mamografia(models.Model):
    NORMAL = 0
    CANCER = 1

    MAMA_RIGHT = 0
    MAMA_LEFT = 1

    LIST_STATE = (
        (NORMAL, "Nornal"),
        (CANCER, "Cancer"),
    )

    LIST_STATE_POS = (
        (MAMA_RIGHT, "Derecha"),
        (MAMA_LEFT, "Izquierda"),
    )

    external_id = models.UUIDField(default=uuid.uuid4, editable=False, null=False)
    resultado = models.PositiveBigIntegerField(
        default=NORMAL, choices=LIST_STATE, blank=False, null=False
    )
    orientacion = models.PositiveBigIntegerField(
        default=MAMA_RIGHT, choices=LIST_STATE_POS, blank=False, null=False
    )
    descripcion = models.CharField(max_length=1024, blank=True, null=True)
    createdAt = models.DateField("CreatedAt", auto_now=True, auto_now_add=False)
    updatedAt = models.DateField("UpdatedAt", auto_now=True, auto_now_add=False)
    paciente = models.ForeignKey(
        Paciente, related_name="paciente", on_delete=models.CASCADE, null=False
    )

    class Meta:
        db_table = "mamografia"
        verbose_name = "mamografia"
        verbose_name_plural = "mamografias"
        ordering = ["pk"]
        
    def toJSON(self):
        item = model_to_dict(self)
        item['external_id'] = self.external_id
        return item

    def __str__(self):
        return str(self.paciente.nombre)


class MamografiaImage(models.Model):
    VERTICAL = 0
    HORIZONTAL = 1
    LIST_STATE = (
        (VERTICAL, "Vertical"),
        (HORIZONTAL, "Horizontal"),
    )

    external_id = models.UUIDField(default=uuid.uuid4, editable=False, null=False)
    imagen = models.ImageField(
        upload_to="mamografia/%Y/%m/%d",
        null=True,
        blank=True,
        verbose_name="mamografia",
    )
    orientacion = models.PositiveBigIntegerField(
        default=(VERTICAL), choices=LIST_STATE, blank=False, null=False
    )
    createdAt = models.DateField("CreatedAt", auto_now=True, auto_now_add=False)
    updatedAt = models.DateField("UpdatedAt", auto_now=True, auto_now_add=False)
    mamografia = models.ForeignKey(
        Mamografia, verbose_name="mamografia", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "mamografia_image"
        verbose_name = "mamografia_image"
        verbose_name_plural = "mamografia_images"
        ordering = ["pk"]


class MamografiaUploadFile(models.Model):
    DERECHA = 0
    IZQUIERDA = 1
    LIST_STATE = (
        (DERECHA, "Derecha"),
        (IZQUIERDA, "Izquierda"),
    )
    
    imagen_horizontal = models.ImageField(
        upload_to="mamografia/%Y/%m/%d",
        null=True,
        blank=True,
        verbose_name="horizontal",
    )
    imagen_vertical = models.ImageField(
        upload_to="mamografia/%Y/%m/%d", null=True, blank=True, verbose_name="vertical"
    )
    lado_mamario = models.PositiveBigIntegerField(
        default=DERECHA, choices=LIST_STATE,
    )
    paciente = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "mamografia_upload"
        verbose_name = "mamografia_upload"
        verbose_name_plural = "mamografia_uploads"
        ordering = ["pk"]


@receiver(pre_save, sender=MamografiaUploadFile)
def pre_save_receiver(sender, instance, **kwargs):
    from apps.modelos.layers.application.service_app_upload_images import (
        MamografiaAppService,
    )

    MamografiaAppService.pre_procesar_datos()


@receiver(post_save, sender=MamografiaUploadFile)
def post_save_receiver(sender, instance, **kwargs):
    from apps.modelos.layers.application.service_app_upload_images import (
        MamografiaAppService,
    )

    MamografiaAppService.procesar_datos(instance)
