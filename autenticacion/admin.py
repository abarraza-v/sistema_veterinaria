from django.contrib import admin
from .models import LoginAttempt, UserProfile


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('username', 'ip_address', 'successful', 'attempted_at')
    list_filter = ('successful', 'attempted_at')
    search_fields = ('username', 'ip_address')
    readonly_fields = ('username', 'ip_address', 'successful', 'attempted_at')
    date_hierarchy = 'attempted_at'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'debe_cambiar_password', 'password_reset_date')
    list_filter = ('debe_cambiar_password',)
    search_fields = ('user__username', 'user__email')
