from datetime import datetime
from django import forms
from apps.modelos.models import *


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "first_name", "last_name", "password"]
        exclude = ["createdAt", "updatedAt"]

        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "id": "email",
                    "class": "input100",
                    "placeholder": "Ingrese el email",
                    "required": "",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "id": "username",
                    "class": "input100",
                    "placeholder": "Ingrese el nombre de usuario",
                    "required": "",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "id": "first_name",
                    "class": "input100",
                    "placeholder": "Ingrese el nombre",
                    "required": "",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "id": "last_name",
                    "class": "input100",
                    "placeholder": "Ingrese el apellido",
                    "required": "",
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "id": "password",
                    "class": "input100",
                    "placeholder": "Ingrese la contraseña",
                    "required": "",
                }
            ),
        }

    password_confirm = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={
                "id": "password_confirm",
                "class": "input100",
                "placeholder": "Verificar contraseña",
                "required": "",
            }
        ),
    )

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password_confirm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class PacienteForm(forms.ModelForm):
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields["cedula"].widget.attrs["autofocus"] = True
        self.fields["cedula"].widget.attrs["required"] = True

    class Meta:
        model = Paciente
        fields = "__all__"
        exclude = ["createdAt", "updatedAt"]
        widgets = {
            "cedula": forms.TextInput(
                attrs={
                    "id": "cedula",
                    "class": "form-control",
                    "placeholder": "Ingrese el nombre de la categoria",
                    "required": True,
                }
            ),
            "nombre": forms.TextInput(
                attrs={
                    "id": "nombre",
                    "class": "form-control",
                    "placeholder": "Ingrese el nombre de la categoria",
                    "required": True,
                }
            ),
            "apellido_paterno": forms.TextInput(
                attrs={
                    "id": "nombre",
                    "class": "form-control",
                    "placeholder": "Ingrese el nombre de la categoria",
                    "required": True,
                }
            ),
            "apellido_materno": forms.TextInput(
                attrs={
                    "id": "nombre",
                    "class": "form-control",
                    "placeholder": "Ingrese el nombre de la categoria",
                    "required": True,
                }
            ),
        }


class MamografiaForm(forms.ModelForm):
    LADO_CHOICES = (
        ("", "Seleccione un lado mamario"),
        (0, "Derecha"),
        (1, "Izquierda"),
    )
    lado_mamario = (
        forms.ChoiceField(
            choices=LADO_CHOICES,
            widget=forms.Select(attrs={"id": "lado_mamario", "class": "form-control"}),
            required=True,
        ),
    )

    class Meta:
        model = Mamografia
        fields = "__all__"
        exclude = ["createdAt", "updatedAt", "paciente"]
        widgets = {
            "resultado": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese el nombre de la categoria",
                    "required": "",
                }
            ),
            "descripcion": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese el nombre de la categoria",
                    "required": "",
                }
            ),
        }


class MamografiaImageForm(forms.ModelForm):
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields["imagen"].widget.attrs["autofocus"] = True
        self.fields["imagen"].widget.attrs["required"] = True

    class Meta:
        model = MamografiaImage
        fields = "__all__"
        exclude = ["createdAt", "updatedAt", "mamografia", ""]
        widgets = {
            "imagen": forms.ClearableFileInput(
                attrs={"class": "form-control", "type": "file"},
            ),
        }


class MamografiaUploadForm(forms.ModelForm):
    """
    Formulario para la subida de mamografias
    """

    LADO_CHOICES = (
        ("", "Seleccione un lado"),
        (0, "derecha"),
        (1, "izquierda"),
    )

    # Define el campo lado_mamario como models.ChoiceField
    lado_mamario = forms.ChoiceField(
        choices=LADO_CHOICES,
        widget=forms.Select(attrs={"id": "lado_mamario", "class": "form-control"}),
        required=True,
    )

    class Meta:
        model = MamografiaUploadFile
        fields = "__all__"
        widgets = {
            "imagen_horizontal": forms.ClearableFileInput(
                attrs={
                    "id": "imagen_horizontal",
                    "class": "form-control",
                    "accept": ".png, .jpg, .jpeg",
                }
            ),
            "imagen_vertical": forms.ClearableFileInput(
                attrs={
                    "id": "imagen_vertical",
                    "class": "form-control",
                    "accept": ".png, .jpg, .jpeg",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "row": "1", "cols": "5"}
            ),
            "paciente": forms.TextInput(
                attrs={
                    "type": "hidden",
                    "id": "paciente",
                    "name": "paciente",
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, external=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if external is not None:
            self.fields["paciente"].initial = external
            self.fields["descripcion"].initial = external
