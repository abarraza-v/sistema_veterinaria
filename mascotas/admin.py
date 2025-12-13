from django.contrib import admin
from .models import Mascota


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'dueno', 'is_deleted', 'created_at')
    list_filter = ('especie', 'sexo', 'is_deleted', 'created_at')
    search_fields = ('nombre', 'raza', 'dueno__nombre')
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')

