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
        widgets = {
            'estado': forms.Select(choices=EstadoCompra.ESTADOS_CHOICES),
        }
        labels = {
            'estado': 'Nuevo estado',  # Cambia el label aquí
        }




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