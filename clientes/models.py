from django.db import models
from django.utils import timezone


class ActiveManager(models.Manager):
    """Manager personalizado que excluye registros eliminados"""
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Cliente(models.Model):
    """Modelo para los clientes de la veterinaria"""
    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nombre} - {self.rut}"

    def soft_delete(self):
        """Realiza un soft delete del cliente"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restaura un cliente eliminado"""
        self.is_deleted = False
        self.deleted_at = None
        self.save()

