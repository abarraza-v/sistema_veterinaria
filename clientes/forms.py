from django import forms
from .models import Cliente
from core.utils import validar_rut, formatear_rut, formatear_telefono_chileno


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'rut', 'telefono', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo',
                'required': True
            }),
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12.345.678-9',
                'required': True,
                'onblur': 'formatRUT(this)'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 8765 4321',
                'required': True,
                'onblur': 'formatPhone(this)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.cl'
            }),
        }
        labels = {
            'nombre': 'Nombre Completo',
            'rut': 'RUT',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico (opcional)',
        }
    
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            if not validar_rut(rut):
                raise forms.ValidationError('El RUT ingresado no es válido.')
            # Formatear el RUT antes de guardarlo
            rut = formatear_rut(rut)
            
            # Verificar que el RUT sea único (excepto para la instancia actual)
            if self.instance.pk:
                # Editando un cliente existente
                if Cliente.objects.filter(rut=rut).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError('Ya existe un cliente con este RUT.')
            else:
                # Creando un nuevo cliente
                if Cliente.objects.filter(rut=rut).exists():
                    raise forms.ValidationError('Ya existe un cliente con este RUT.')
        return rut
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Formatear el teléfono antes de guardarlo
            telefono = formatear_telefono_chileno(telefono)
            
            # Validar formato básico (debe tener al menos 8 dígitos)
            import re
            digitos = re.sub(r'\D', '', telefono)
            if len(digitos) < 8:
                raise forms.ValidationError('El teléfono debe tener al menos 8 dígitos.')
        return telefono
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Verificar que el email sea único (excepto para la instancia actual)
            if self.instance.pk:
                # Editando un cliente existente
                if Cliente.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError('Ya existe un cliente con este correo electrónico.')
            else:
                # Creando un nuevo cliente
                if Cliente.objects.filter(email__iexact=email).exists():
                    raise forms.ValidationError('Ya existe un cliente con este correo electrónico.')
        return email
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            # Validar que el nombre tenga al menos 3 caracteres
            if len(nombre.strip()) < 3:
                raise forms.ValidationError('El nombre debe tener al menos 3 caracteres.')
            # Validar que no sea solo números
            if nombre.strip().isdigit():
                raise forms.ValidationError('El nombre no puede contener solo números.')
        return nombre
