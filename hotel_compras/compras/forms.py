from django import forms
from .models import SolicitudCompra, EstadoCompra
from .models import Profile, Departamento
from django.contrib.auth.models import User


class SolicitudCompraForm(forms.ModelForm):
    class Meta:
        model = SolicitudCompra
        fields = ['descripcion']

# En forms.py

class EstadoCompraForm(forms.ModelForm):
    class Meta:
        model = EstadoCompra
        fields = ['estado']
        labels = {
            'estado': 'Nuevo estado',  # Cambia el label aquí
        }

    def __init__(self, *args, **kwargs):
        solicitud = kwargs.pop('solicitud', None)
        super().__init__(*args, **kwargs)
        if solicitud:
            siguiente_estado = solicitud.siguiente_estado()
            if siguiente_estado:
                self.fields['estado'].choices = [(siguiente_estado, siguiente_estado)]
            else:
                self.fields['estado'].choices = []  # O manejar de otra manera cuando no hay más estados



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['departamento']

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['nombre']