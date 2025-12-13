from django.contrib import admin
from .models import LoginAttempt


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
