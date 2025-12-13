from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
import secrets
import string


class UsuarioForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Rol'
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'grupo']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.cl',
                'required': True
            }),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando, cargar el grupo actual
        if self.instance.pk:
            user_groups = self.instance.groups.all()
            if user_groups.exists():
                self.fields['grupo'].initial = user_groups.first()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verificar que el email sea único
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Si es un nuevo usuario, generar username y contraseña
        if not user.pk:
            # Generar username a partir del email
            user.username = self.cleaned_data['email'].split('@')[0]
            
            # Si el username ya existe, agregar un número
            base_username = user.username
            counter = 1
            while User.objects.filter(username=user.username).exists():
                user.username = f"{base_username}{counter}"
                counter += 1
            
            # Generar contraseña aleatoria
            password = self.generate_password()
            user.set_password(password)
            user.is_staff = True
            
            # Guardar la contraseña generada para enviarla por email
            user._generated_password = password
        
        if commit:
            user.save()
            
            # Asignar al grupo seleccionado
            grupo = self.cleaned_data['grupo']
            user.groups.clear()
            user.groups.add(grupo)
        
        return user
    
    def generate_password(self, length=12):
        """Genera una contraseña aleatoria segura"""
        characters = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
