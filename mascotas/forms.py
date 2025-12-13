from django import forms
from django.utils import timezone
from datetime import date
from .models import Mascota
from clientes.models import Cliente


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['dueno', 'nombre', 'especie', 'especie_otro', 'raza', 'sexo', 'edad', 'fecha_nacimiento', 'alergias']
        widgets = {
            'dueno': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la mascota',
                'required': True
            }),
            'especie': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'id': 'id_especie'
            }),
            'especie_otro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Especificar especie',
                'id': 'id_especie_otro'
            }),
            'raza': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Raza de la mascota',
                'required': True
            }),
            'sexo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'edad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Edad en años (calculada automáticamente)',
                'min': 0,
                'step': '0.1',
                'id': 'id_edad',
                'readonly': True
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'id_fecha_nacimiento'
            },
            format='%Y-%m-%d'),
            'alergias': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describa las alergias si las tiene',
                'rows': 3
            }),
        }
        labels = {
            'dueno': 'Dueño',
            'nombre': 'Nombre de la Mascota',
            'especie': 'Especie',
            'especie_otro': 'Especificar Otra Especie',
            'raza': 'Raza',
            'sexo': 'Sexo',
            'edad': 'Edad (años)',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'alergias': 'Alergias',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo clientes activos
        self.fields['dueno'].queryset = Cliente.objects.filter(is_deleted=False).order_by('nombre')
        
        # Establecer el formato de fecha
        self.fields['fecha_nacimiento'].input_formats = ['%Y-%m-%d']
        
        # Si hay una instancia con fecha de nacimiento, deshabilitar campo edad
        if self.instance and self.instance.pk and self.instance.fecha_nacimiento:
            self.fields['edad'].widget.attrs['readonly'] = True
        else:
            self.fields['edad'].widget.attrs.pop('readonly', None)
    
    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento:
            # No permitir fechas futuras
            if fecha_nacimiento > date.today():
                raise forms.ValidationError('La fecha de nacimiento no puede ser posterior a hoy.')
        return fecha_nacimiento
    
    def clean(self):
        cleaned_data = super().clean()
        especie = cleaned_data.get('especie')
        especie_otro = cleaned_data.get('especie_otro')
        
        # Si la especie es "Otro", el campo especie_otro es obligatorio
        if especie == 'Otro' and not especie_otro:
            self.add_error('especie_otro', 'Debe especificar la especie.')
        
        return cleaned_data
    
    def save(self, commit=True):
        mascota = super().save(commit=False)
        
        # Calcular edad automáticamente si hay fecha de nacimiento
        if mascota.fecha_nacimiento:
            today = date.today()
            # Calcular edad en años
            edad_years = today.year - mascota.fecha_nacimiento.year
            edad_months = today.month - mascota.fecha_nacimiento.month
            
            # Ajustar si no ha cumplido años este año
            if edad_months < 0 or (edad_months == 0 and today.day < mascota.fecha_nacimiento.day):
                edad_years -= 1
                edad_months += 12
            
            if today.day < mascota.fecha_nacimiento.day and edad_months > 0:
                edad_months -= 1
            
            # Convertir a decimal
            edad_decimal = edad_years + (edad_months / 12.0)
            
            # Si es un número entero, guardarlo sin decimales
            if edad_decimal == int(edad_decimal):
                mascota.edad = int(edad_decimal)
            else:
                mascota.edad = round(edad_decimal, 1)
        
        if commit:
            mascota.save()
        return mascota
