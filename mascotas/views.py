from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Mascota
from .forms import MascotaForm


@login_required
def listar(request):
    """Redirige a la vista unificada de clientes"""
    return redirect('clientes:listar' + '?tab=mascotas')


@login_required
def crear(request):
    """Crear una nueva mascota"""
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            mascota = form.save()
            messages.success(request, f'Mascota "{mascota.nombre}" registrada exitosamente.')
            return redirect('clientes:listar')
    else:
        form = MascotaForm()
    
    return render(request, 'mascotas/mascota_form.html', {
        'form': form,
        'title': 'Registrar Mascota',
        'button_text': 'Registrar Mascota'
    })


@login_required
def editar(request, pk):
    """Editar una mascota existente"""
    mascota = get_object_or_404(Mascota, pk=pk, is_deleted=False)
    
    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            mascota = form.save()
            messages.success(request, f'Mascota "{mascota.nombre}" actualizada exitosamente.')
            return redirect('clientes:listar')
    else:
        form = MascotaForm(instance=mascota)
    
    return render(request, 'mascotas/mascota_form.html', {
        'form': form,
        'mascota': mascota,
        'title': 'Editar Mascota',
        'button_text': 'Guardar Cambios'
    })


@login_required
def eliminar(request, pk):
    """Soft delete de una mascota (solo administradores)"""
    # Verificar que el usuario sea administrador
    if not request.user.groups.filter(name='Administrador').exists():
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('clientes:listar')
    
    mascota = get_object_or_404(Mascota, pk=pk)
    
    if request.method == 'POST':
        # Realizar soft delete
        mascota.soft_delete()
        messages.success(request, f'Mascota "{mascota.nombre}" eliminada exitosamente.')
        return redirect('clientes:listar')
    
    return render(request, 'mascotas/mascota_confirm_delete.html', {
        'mascota': mascota
    })


