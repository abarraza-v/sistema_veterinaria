from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def listar(request):
    return render(request, 'mascotas/mascota_list.html')


@login_required
def crear(request):
    return render(request, 'mascotas/mascota_form.html')


@login_required
def editar(request, pk):
    return render(request, 'mascotas/mascota_form.html')


@login_required
def eliminar(request, pk):
    return render(request, 'mascotas/mascota_confirm_delete.html')

