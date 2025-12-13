from django import forms
from django.contrib.auth import authenticate
from .models import LoginAttempt


class LoginForm(forms.Form):
    """Formulario de autenticación"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.cl',
            'id': 'id_username'
        }),
        label='Usuario / Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••',
            'id': 'id_password'
        }),
        label='Contraseña'
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'remember_me'
        }),
        label='Recordar sesión'
    )
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            # Verificar si el usuario está bloqueado
            if LoginAttempt.is_locked(username):
                time_remaining = LoginAttempt.get_lockout_time_remaining(username)
                minutes = time_remaining // 60
                seconds = time_remaining % 60
                raise forms.ValidationError(
                    f'Cuenta bloqueada temporalmente. Intenta nuevamente en {minutes}:{seconds:02d} minutos.'
                )
            
            # Intentar autenticar
            user = authenticate(
                request=self.request,
                username=username,
                password=password
            )
            
            if user is None:
                # Intentar con el email si no funcionó el username
                from django.contrib.auth.models import User
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(
                        request=self.request,
                        username=user_obj.username,
                        password=password
                    )
                except User.DoesNotExist:
                    pass
            
            if user is None:
                # Registrar intento fallido
                if self.request:
                    ip = self.get_client_ip()
                    LoginAttempt.objects.create(
                        username=username,
                        ip_address=ip,
                        successful=False
                    )
                
                remaining = LoginAttempt.get_remaining_attempts(username)
                if remaining > 0:
                    raise forms.ValidationError(
                        f'Usuario o contraseña incorrectos. Te quedan {remaining} intentos.'
                    )
                else:
                    raise forms.ValidationError(
                        'Cuenta bloqueada temporalmente por múltiples intentos fallidos.'
                    )
            
            if not user.is_active:
                raise forms.ValidationError('Esta cuenta está desactivada.')
            
            cleaned_data['user'] = user
        
        return cleaned_data
    
    def get_client_ip(self):
        """Obtiene la IP del cliente"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR', '0.0.0.0')
        return ip
