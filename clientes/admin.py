from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'telefono', 'email', 'is_deleted', 'created_at')
    list_filter = ('is_deleted', 'created_at')
    search_fields = ('nombre', 'rut', 'telefono', 'email')
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')

