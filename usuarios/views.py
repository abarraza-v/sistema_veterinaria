from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import UsuarioForm
import secrets
import string


def is_admin(user):
    """Verifica si el usuario es administrador"""
    return user.groups.filter(name='Administrador').exists()


@login_required
@user_passes_test(is_admin, login_url='clientes:listar')
def listar(request):
    """Lista todos los usuarios del sistema (solo administradores)"""
    usuarios = User.objects.filter(is_superuser=False).prefetch_related('groups').order_by('-date_joined')
    
    return render(request, 'usuarios/usuario_list.html', {
        'usuarios': usuarios
    })


@login_required
@user_passes_test(is_admin, login_url='clientes:listar')
def crear(request):
    """Crear un nuevo usuario (solo administradores)"""
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            
            # Enviar email con credenciales
            if hasattr(usuario, '_generated_password'):
                enviar_credenciales(usuario, usuario._generated_password)
                messages.success(
                    request, 
                    f'Usuario "{usuario.get_full_name()}" creado exitosamente. '
                    f'Las credenciales han sido enviadas a {usuario.email}.'
                )
            else:
                messages.success(request, f'Usuario "{usuario.get_full_name()}" creado exitosamente.')
            
            return redirect('usuarios:listar')
    else:
        form = UsuarioForm()
    
    return render(request, 'usuarios/usuario_form.html', {
        'form': form,
        'title': 'Nuevo Usuario',
        'button_text': 'Crear Usuario'
    })


@login_required
@user_passes_test(is_admin, login_url='clientes:listar')
def editar(request, pk):
    """Editar un usuario existente (solo administradores)"""
    usuario = get_object_or_404(User, pk=pk, is_superuser=False)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario "{usuario.get_full_name()}" actualizado exitosamente.')
            return redirect('usuarios:listar')
    else:
        form = UsuarioForm(instance=usuario)
    
    return render(request, 'usuarios/usuario_form.html', {
        'form': form,
        'usuario': usuario,
        'title': 'Editar Usuario',
        'button_text': 'Guardar Cambios'
    })


@login_required
@user_passes_test(is_admin, login_url='clientes:listar')
def toggle_active(request, pk):
    """Activar/Desactivar un usuario (solo administradores)"""
    usuario = get_object_or_404(User, pk=pk, is_superuser=False)
    
    # No permitir desactivar el propio usuario
    if usuario == request.user:
        messages.error(request, 'No puedes desactivar tu propia cuenta.')
        return redirect('usuarios:listar')
    
    if request.method == 'POST':
        usuario.is_active = not usuario.is_active
        usuario.save()
        
        estado = 'activado' if usuario.is_active else 'desactivado'
        messages.success(request, f'Usuario "{usuario.get_full_name()}" {estado} exitosamente.')
        return redirect('usuarios:listar')
    
    return render(request, 'usuarios/usuario_toggle_confirm.html', {
        'usuario': usuario
    })


@login_required
@user_passes_test(is_admin, login_url='clientes:listar')
def reset_password(request, pk):
    """Restablecer contraseña de un usuario (solo administradores)"""
    usuario = get_object_or_404(User, pk=pk, is_superuser=False)
    
    if request.method == 'POST':
        # Generar nueva contraseña
        nueva_password = generar_password()
        usuario.set_password(nueva_password)
        usuario.save()
        
        # Enviar email con la nueva contraseña
        enviar_nueva_password(usuario, nueva_password)
        
        messages.success(
            request,
            f'Contraseña restablecida para "{usuario.get_full_name()}". '
            f'Las nuevas credenciales han sido enviadas a {usuario.email}.'
        )
        return redirect('usuarios:listar')
    
    return render(request, 'usuarios/usuario_reset_password_confirm.html', {
        'usuario': usuario
    })


def generar_password(length=12):
    """Genera una contraseña aleatoria segura"""
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


def enviar_credenciales(usuario, password):
    """Envía las credenciales de acceso por email"""
    asunto = 'Credenciales de acceso - Veterinaria Patitas Felices'
    mensaje = f"""
Hola {usuario.get_full_name()},

Tu cuenta en Veterinaria Patitas Felices ha sido creada exitosamente.

Credenciales de acceso:
Email: {usuario.email}
Contraseña: {password}

Por favor, cambia tu contraseña al iniciar sesión por primera vez.

Saludos,
Veterinaria Patitas Felices
    """
    
    try:
        send_mail(
            asunto,
            mensaje,
            settings.EMAIL_HOST_USER,
            [usuario.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error al enviar email: {e}")


def enviar_nueva_password(usuario, password):
    """Envía la nueva contraseña por email"""
    asunto = 'Contraseña restablecida - Veterinaria Patitas Felices'
    mensaje = f"""
Hola {usuario.get_full_name()},

Tu contraseña ha sido restablecida.

Nuevas credenciales de acceso:
Email: {usuario.email}
Contraseña: {password}

Por favor, cambia tu contraseña al iniciar sesión.

Saludos,
Veterinaria Patitas Felices
    """
    
    try:
        send_mail(
            asunto,
            mensaje,
            settings.EMAIL_HOST_USER,
            [usuario.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error al enviar email: {e}")


