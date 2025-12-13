from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class LoginAttempt(models.Model):
    """
    Modelo para rastrear intentos de login fallidos
    """
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
    attempted_at = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Intento de Login'
        verbose_name_plural = 'Intentos de Login'
        ordering = ['-attempted_at']
    
    def __str__(self):
        return f"{self.username} - {self.attempted_at} - {'Exitoso' if self.successful else 'Fallido'}"
    
    @classmethod
    def is_locked(cls, username):
        """
        Verifica si un usuario está bloqueado por intentos fallidos
        """
        time_threshold = timezone.now() - timedelta(minutes=5)
        
        # Contar intentos fallidos en los últimos 5 minutos
        failed_attempts = cls.objects.filter(
            username=username,
            successful=False,
            attempted_at__gte=time_threshold
        ).count()
        
        return failed_attempts >= 5
    
    @classmethod
    def get_remaining_attempts(cls, username):
        """
        Retorna el número de intentos restantes antes del bloqueo
        """
        time_threshold = timezone.now() - timedelta(minutes=5)
        
        failed_attempts = cls.objects.filter(
            username=username,
            successful=False,
            attempted_at__gte=time_threshold
        ).count()
        
        return max(0, 5 - failed_attempts)
    
    @classmethod
    def get_lockout_time_remaining(cls, username):
        """
        Retorna el tiempo restante de bloqueo en segundos
        """
        time_threshold = timezone.now() - timedelta(minutes=5)
        
        oldest_failed = cls.objects.filter(
            username=username,
            successful=False,
            attempted_at__gte=time_threshold
        ).order_by('attempted_at').first()
        
        if not oldest_failed:
            return 0
        
        unlock_time = oldest_failed.attempted_at + timedelta(minutes=5)
        remaining = (unlock_time - timezone.now()).total_seconds()
        
        return max(0, int(remaining))


class UserProfile(models.Model):
    """
    Perfil extendido para usuarios con información adicional
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    debe_cambiar_password = models.BooleanField(default=False)
    password_reset_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'
    
    def __str__(self):
        return f"Perfil de {self.user.username}"

