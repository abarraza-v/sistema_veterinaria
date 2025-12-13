from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import LoginForm
from .models import LoginAttempt


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Vista para el login de usuarios"""
    
    # Si el usuario ya está autenticado, redirigir
    if request.user.is_authenticated:
        return redirect('clientes:listar')
    
    if request.method == 'POST':
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            user = form.cleaned_data['user']
            
            # Registrar intento exitoso
            ip = form.get_client_ip()
            LoginAttempt.objects.create(
                username=user.username,
                ip_address=ip,
                successful=True
            )
            
            # Iniciar sesión
            login(request, user)
            
            # Manejar "recordar sesión"
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)  # Sesión expira al cerrar el navegador
            
            messages.success(request, f'Bienvenido, {user.first_name}!')
            return redirect('clientes:listar')
    else:
        form = LoginForm()
    
    return render(request, 'autenticacion/login.html', {
        'form': form
    })


def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('autenticacion:login')

