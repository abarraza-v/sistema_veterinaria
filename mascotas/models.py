from django.db import models
from django.utils import timezone
from clientes.models import Cliente


class ActiveManager(models.Manager):
    """Manager personalizado que excluye registros eliminados"""
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Mascota(models.Model):
    """Modelo para las mascotas de los clientes"""
    
    ESPECIES_CHOICES = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Ave', 'Ave'),
        ('Roedor', 'Roedor'),
        ('Reptil', 'Reptil'),
        ('Otro', 'Otro'),
    ]
    
    SEXO_CHOICES = [
        ('Macho', 'Macho'),
        ('Hembra', 'Hembra'),
    ]
    
    dueno = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mascotas')
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50, choices=ESPECIES_CHOICES)
    especie_otro = models.CharField(max_length=50, blank=True, null=True)
    raza = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    edad = models.IntegerField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nombre} ({self.especie}) - {self.dueno.nombre}"

    def soft_delete(self):
        """Realiza un soft delete de la mascota"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restaura una mascota eliminada"""
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def get_especie_display_custom(self):
        """Retorna la especie, usando especie_otro si aplica"""
        if self.especie == 'Otro' and self.especie_otro:
            return self.especie_otro
        return self.especie

