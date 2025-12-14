from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.listar, name='listar'),
    path('crear/', views.crear, name='crear'),
    path('editar/<int:pk>/', views.editar, name='editar'),
    path('toggle/<int:pk>/', views.toggle_active, name='toggle_active'),
    path('reset_password/<int:pk>/', views.reset_password, name='reset_password'),
    path('cambiar_password/<int:pk>/', views.cambiar_password, name='cambiar_password'),
    path('detalle/<int:pk>/', views.detalle, name='detalle'),
]
