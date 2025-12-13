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
        return rut
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Formatear el teléfono antes de guardarlo
            telefono = formatear_telefono_chileno(telefono)
        return telefono
