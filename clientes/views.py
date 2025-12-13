from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from .models import Cliente
from .forms import ClienteForm


@login_required
def listar(request):
    """Vista unificada de Clientes y Mascotas con switch de pestañas"""
    query = request.GET.get('q', '')
    tab = request.GET.get('tab', 'clientes')  # 'clientes' o 'mascotas'
    
    # Obtener clientes
    clientes = Cliente.objects.annotate(
        num_mascotas=Count('mascotas', filter=Q(mascotas__is_deleted=False))
    ).order_by('-created_at')
    
    if query and tab == 'clientes':
        clientes = clientes.filter(
            Q(nombre__icontains=query) |
            Q(rut__icontains=query) |
            Q(telefono__icontains=query) |
            Q(email__icontains=query)
        )
    
    # Obtener mascotas
    from mascotas.models import Mascota
    mascotas = Mascota.objects.select_related('dueno').order_by('-created_at')
    
    if query and tab == 'mascotas':
        mascotas = mascotas.filter(
            Q(nombre__icontains=query) |
            Q(dueno__nombre__icontains=query) |
            Q(especie__icontains=query) |
            Q(raza__icontains=query)
        )
    
    context = {
        'clientes': clientes,
        'mascotas': mascotas,
        'query': query,
        'tab': tab,
    }
    
    return render(request, 'clientes/clientes_mascotas.html', context)


@login_required
def crear(request):
    """Crear un nuevo cliente"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nombre}" creado exitosamente.')
            return redirect('clientes:listar')
    else:
        form = ClienteForm()
    
    return render(request, 'clientes/cliente_form.html', {
        'form': form,
        'title': 'Registrar Cliente',
        'button_text': 'Registrar Cliente'
    })


@login_required
def editar(request, pk):
    """Editar un cliente existente"""
    cliente = get_object_or_404(Cliente, pk=pk, is_deleted=False)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nombre}" actualizado exitosamente.')
            return redirect('clientes:listar')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'clientes/cliente_form.html', {
        'form': form,
        'cliente': cliente,
        'title': 'Editar Cliente',
        'button_text': 'Guardar Cambios'
    })


@login_required
def eliminar(request, pk):
    """Soft delete de un cliente (solo administradores)"""
    # Verificar que el usuario sea administrador
    if not request.user.groups.filter(name='Administrador').exists():
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('clientes:listar')
    
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        # Realizar soft delete
        cliente.soft_delete()
        messages.success(request, f'Cliente "{cliente.nombre}" eliminado exitosamente.')
        return redirect('clientes:listar')
    
    # Contar mascotas asociadas
    num_mascotas = cliente.mascotas.filter(is_deleted=False).count()
    
    return render(request, 'clientes/cliente_confirm_delete.html', {
        'cliente': cliente,
        'num_mascotas': num_mascotas
    })


