from django.db import models
from django.contrib.auth.models import User

class SolicitudCompra(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.TextField()
    estado = models.CharField(max_length=100, default='Solicitado')
    departamento = models.ForeignKey('Departamento', on_delete=models.SET_NULL, null=True, blank=True)  # Nuevo campo

    def __str__(self):
        return f'Solicitud de compra #{self.id}'

# En models.py

class EstadoCompra(models.Model):
    ESTADOS_CHOICES = [
        ('Solicitado', 'Solicitado'),
        ('Aprobado', 'Aprobado'),
        ('En Proceso', 'En Proceso'),
        ('Finalizado', 'Finalizado'),
        ('Cancelado', 'Cancelado'),
    ]

    solicitud = models.ForeignKey(SolicitudCompra, on_delete=models.CASCADE)
    estado = models.CharField(max_length=100, choices=ESTADOS_CHOICES)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    actualizado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.estado} - {self.solicitud}'


class Departamento(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

