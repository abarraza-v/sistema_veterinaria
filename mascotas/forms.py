from django import forms
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
                'placeholder': 'Edad en años',
                'min': 0
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
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
    
    def clean(self):
        cleaned_data = super().clean()
        especie = cleaned_data.get('especie')
        especie_otro = cleaned_data.get('especie_otro')
        
        # Si la especie es "Otro", el campo especie_otro es obligatorio
        if especie == 'Otro' and not especie_otro:
            self.add_error('especie_otro', 'Debe especificar la especie.')
        
        return cleaned_data
