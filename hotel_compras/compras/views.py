from django.shortcuts import render, get_object_or_404, redirect
from .models import SolicitudCompra, EstadoCompra,Profile,Departamento
from .forms import SolicitudCompraForm, EstadoCompraForm ,DepartamentoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserForm, ProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import ProfileForm  # Asegúrate de que este formulario esté definido en tu archivo forms.py
from .models import Profile

def lista_solicitudes(request):
    if request.user.is_superuser:
        solicitudes = SolicitudCompra.objects.all()
    else:
        perfil = Profile.objects.get(user=request.user)
        if perfil.departamento:
            solicitudes = SolicitudCompra.objects.filter(solicitante__profile__departamento=perfil.departamento)
        else:
            solicitudes = SolicitudCompra.objects.none()  # O manejarlo de otra manera apropiada

    return render(request, 'lista_solicitudes.html', {'solicitudes': solicitudes})
def detalle_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudCompra, pk=solicitud_id)
    estados = EstadoCompra.objects.filter(solicitud=solicitud)
    return render(request, 'detalle_solicitud.html', {'solicitud': solicitud, 'estados': estados})

# Otras vistas para crear, actualizar y eliminar solicitudes y estados
@login_required
def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudCompraForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.solicitante = request.user
            solicitud.departamento = request.user.profile.departamento  # Asignar departamento
            solicitud.save()
            # Crear el primer estado de la solicitud (ej. Solicitado)
            EstadoCompra.objects.create(solicitud=solicitud, estado='Solicitado', actualizado_por=request.user)
            return redirect('lista_solicitudes')
    else:
        form = SolicitudCompraForm()
    
    return render(request, 'crear_solicitud.html', {'form': form})

@login_required
def actualizar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudCompra, pk=solicitud_id)
    
    if request.method == 'POST':
        form = EstadoCompraForm(request.POST, solicitud=solicitud)
        if form.is_valid():
            estado_nuevo = form.save(commit=False)
            estado_nuevo.solicitud = solicitud
            estado_nuevo.actualizado_por = request.user
            estado_nuevo.save()
            # Actualizar el estado en la solicitud principal también (opcional)
            solicitud.estado = estado_nuevo.estado
            solicitud.save()
            return redirect('detalle_solicitud', solicitud_id=solicitud.id)
    else:
        form = EstadoCompraForm(solicitud=solicitud)
    
    return render(request, 'actualizar_solicitud.html', {'form': form, 'solicitud': solicitud, 'estado_actual': solicitud.estado})


@login_required
def eliminar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudCompra, pk=solicitud_id)
    
    if request.method == 'POST':
        solicitud.delete()
        messages.success(request, 'La solicitud se ha eliminado correctamente.')
        return redirect('lista_solicitudes')
    
    return render(request, 'eliminar_solicitud.html', {'solicitud': solicitud})



@login_required
def crear_usuario(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            try:
                user = user_form.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                messages.success(request, 'Usuario creado exitosamente.')
                return redirect('lista_solicitudes')
            except IntegrityError:
                messages.error(request, 'El usuario ya tiene un perfil.')
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    
    return render(request, 'crear_usuario.html', {'user_form': user_form, 'profile_form': profile_form})
# en views.py
@login_required
def crear_departamento(request):
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_departamentos')
    else:
        form = DepartamentoForm()
    return render(request, 'crear_departamento.html', {'form': form})

@login_required
def lista_departamentos(request):
    departamentos = Departamento.objects.all()
    departamento_solicitudes = {}

    for departamento in departamentos:
        solicitudes = SolicitudCompra.objects.filter(solicitante__profile__departamento=departamento)
        departamento_solicitudes[departamento] = solicitudes

    return render(request, 'lista_departamentos.html', {'departamento_solicitudes': departamento_solicitudes})

