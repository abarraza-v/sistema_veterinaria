from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def listar(request):
    return render(request, 'usuarios/usuario_list.html')


@login_required
def crear(request):
    return render(request, 'usuarios/usuario_form.html')


@login_required
def editar(request, pk):
    return render(request, 'usuarios/usuario_form.html')


@login_required
def toggle_active(request, pk):
    return render(request, 'usuarios/usuario_list.html')


@login_required
def reset_password(request, pk):
    return render(request, 'usuarios/usuario_list.html')

