# 🐾 Sistema Veterinaria "Patitas Felices"

> Sistema de gestión veterinaria desarrollado en Django para administrar clientes, mascotas y usuarios del sistema.

[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 Índice

- [¿Qué es este proyecto?](#qué-es-este-proyecto)
- [Características principales](#características-principales)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Instalación rápida](#instalación-rápida)
- [Uso del sistema](#uso-del-sistema)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Guía para desarrolladores](#guía-para-desarrolladores)
- [Documentación técnica](#documentación-técnica)
- [FAQ](#faq)
- [Contribuir](#contribuir)

---

## 🎯 ¿Qué es este proyecto?

**Veterinaria "Patitas Felices"** es un sistema web completo para gestionar las operaciones diarias de una clínica veterinaria. Permite registrar y administrar:

- 👥 **Clientes** (dueños de mascotas)
- 🐶 **Mascotas** (pacientes de la veterinaria)
- 🔐 **Usuarios** del sistema (administradores, recepcionistas, veterinarios)

### ¿Para quién es?

- **Clínicas veterinarias pequeñas y medianas** que necesitan digitalizar sus procesos
- **Estudiantes** que quieren aprender desarrollo web con Django
- **Desarrolladores** buscando un proyecto base para sistemas de gestión

---

## ✨ Características Principales

### 🔒 Seguridad y Autenticación

- ✅ Sistema de login con bloqueo automático tras 5 intentos fallidos
- ✅ Recuperación de contraseña por email
- ✅ Roles de usuario (Administrador, Recepcionista, Veterinario)
- ✅ Forzar cambio de contraseña en primer login
- ✅ Registro de intentos de acceso con IP

### 👥 Gestión de Clientes

- ✅ Registro de clientes con validación de RUT chileno
- ✅ Formateo automático de RUT (12.345.678-9) y teléfonos (+56 9 8765 4321)
- ✅ Búsqueda por nombre, RUT, teléfono o email
- ✅ Visualización de mascotas asociadas
- ✅ Eliminación lógica (soft delete) para auditoría

### 🐾 Gestión de Mascotas

- ✅ Registro de múltiples mascotas por cliente
- ✅ Especies predefinidas: Perro, Gato, Ave, Roedor, Reptil, Otro
- ✅ Cálculo automático de edad basado en fecha de nacimiento
- ✅ Registro de alergias
- ✅ Búsqueda por nombre, dueño, especie o raza

### 🛡️ Administración de Usuarios

- ✅ Creación de usuarios con contraseñas seguras generadas automáticamente
- ✅ Envío de credenciales por email
- ✅ Activar/desactivar usuarios
- ✅ Resetear contraseñas
- ✅ Asignación de roles y permisos

### 🎨 Interfaz de Usuario

- ✅ Diseño moderno y responsive (Bootstrap 5)
- ✅ Sidebar de navegación con información del usuario
- ✅ Reloj en tiempo real
- ✅ Mensajes flash con auto-cierre
- ✅ Modales AJAX para detalles rápidos
- ✅ Tabs para alternar entre Clientes y Mascotas

---

## 🛠️ Tecnologías Utilizadas

### Backend

| Tecnología          | Versión | Propósito                       |
| ------------------- | ------- | ------------------------------- |
| **Python**          | 3.8+    | Lenguaje de programación        |
| **Django**          | 4.2.x   | Framework web                   |
| **SQLite**          | 3.x     | Base de datos (desarrollo)      |
| **python-decouple** | 3.8     | Gestión de variables de entorno |

### Frontend

| Tecnología             | Versión | Propósito      |
| ---------------------- | ------- | -------------- |
| **Bootstrap**          | 5.3     | Framework CSS  |
| **Bootstrap Icons**    | 1.11    | Iconos         |
| **JavaScript Vanilla** | ES6     | Interactividad |

### Arquitectura

- **Patrón:** MVT (Model-View-Template) de Django
- **Renderizado:** Server-Side Rendering (SSR)
- **Base de datos:** SQLite (dev), PostgreSQL recomendado (producción)

---

## 🚀 Instalación Rápida

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/abarraza-v/sistema_veterinaria.git
cd sistema_veterinaria
```

### Paso 2: Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```ini
SECRET_KEY=tu-secret-key-super-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (opcional para recuperación de contraseña)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
```

### Paso 5: Aplicar migraciones

```bash
python manage.py migrate
```

### Paso 6: Cargar datos de prueba (opcional)

```bash
python manage.py seed
```

Este comando crea:

- 5 usuarios de prueba
- 4 clientes de prueba
- 6 mascotas de prueba
- 3 grupos de permisos

### Paso 7: Iniciar el servidor

```bash
python manage.py runserver
```

### Paso 8: Acceder al sistema

Abrir navegador en: **http://localhost:8000**

---

## 🔑 Credenciales de Acceso (datos de prueba)

| Rol               | Email                    | Contraseña   | Permisos                               |
| ----------------- | ------------------------ | ------------ | -------------------------------------- |
| **Administrador** | admin@vetclinic.cl       | admin123     | Acceso total, puede eliminar registros |
| **Recepcionista** | recepcion@vetclinic.cl   | recepcion123 | Ver, crear, editar (no eliminar)       |
| **Veterinario**   | veterinario@vetclinic.cl | vet123       | Ver, crear, editar (no eliminar)       |

---

## 📱 Uso del Sistema

### 1. Login

![Login](docs/screenshots/login.png)

- Ingresar email o username
- Máximo 5 intentos fallidos (bloqueo temporal de 5 minutos)
- Opción "Recordar sesión"

### 2. Gestión de Clientes y Mascotas

![Clientes](docs/screenshots/clientes.png)

- Alternar entre pestañas "Clientes" y "Mascotas"
- Buscar por nombre, RUT, teléfono, email
- Ver detalles en modal (clic en nombre)
- Crear nuevo cliente/mascota (botón verde)
- Editar (icono lápiz)
- Eliminar (icono basura, solo admins)

### 3. Registrar Cliente

![Formulario Cliente](docs/screenshots/cliente_form.png)

- RUT se valida automáticamente (algoritmo Módulo 11)
- RUT se formatea mientras escribes: 12.345.678-9
- Teléfono se formatea: +56 9 8765 4321
- Email opcional pero debe ser único

### 4. Registrar Mascota

![Formulario Mascota](docs/screenshots/mascota_form.png)

- Seleccionar dueño de lista desplegable
- Si especie es "Otro", aparece campo adicional
- Edad se calcula automáticamente si ingresas fecha de nacimiento
- Alergias opcional

### 5. Gestión de Usuarios (solo Administradores)

![Usuarios](docs/screenshots/usuarios.png)

- Crear nuevo usuario con rol
- Sistema genera contraseña segura automáticamente
- Envía credenciales por email
- Activar/desactivar usuarios
- Resetear contraseña

---

## 📂 Estructura del Proyecto

```
sistema_veterinaria/
│
├── manage.py                      # CLI de Django
├── requirements.txt               # Dependencias Python
├── README.md                      # Este archivo
├── AUDITORIA_TECNICA.md          # Documentación técnica completa
├── QUICKSTART.md                 # Guía de inicio rápido
│
├── sistema_veterinaria/          # Configuración principal
│   ├── settings.py               # Configuración Django
│   ├── urls.py                   # Routing principal
│   └── wsgi.py                   # Servidor WSGI
│
├── core/                         # Utilidades compartidas
│   ├── utils.py                  # Validadores de RUT, teléfono, etc.
│   └── management/commands/
│       └── seed.py               # Comando para poblar BD
│
├── autenticacion/                # Sistema de login
│   ├── models.py                 # LoginAttempt, UserProfile
│   ├── views.py                  # login_view, logout_view
│   ├── forms.py                  # LoginForm
│   └── templates/autenticacion/
│       ├── login.html
│       └── password_reset_*.html
│
├── clientes/                     # Gestión de clientes
│   ├── models.py                 # Cliente (con soft delete)
│   ├── views.py                  # CRUD de clientes
│   ├── forms.py                  # ClienteForm
│   └── templates/clientes/
│       ├── clientes_mascotas.html  # Vista unificada
│       └── cliente_form.html
│
├── mascotas/                     # Gestión de mascotas
│   ├── models.py                 # Mascota (con soft delete)
│   ├── views.py                  # CRUD de mascotas
│   ├── forms.py                  # MascotaForm
│   └── templates/mascotas/
│       └── mascota_form.html
│
├── usuarios/                     # Administración de usuarios
│   ├── views.py                  # CRUD, reset password
│   ├── forms.py                  # UsuarioForm
│   └── templates/usuarios/
│       ├── usuario_list.html
│       └── usuario_form.html
│
├── templates/                    # Templates base
│   ├── base.html                 # HTML base
│   └── base_with_sidebar.html    # Base + sidebar
│
└── static/                       # Archivos estáticos
    ├── css/
    │   ├── main.css              # Estilos generales
    │   ├── sidebar.css           # Estilos del sidebar
    │   └── forms.css             # Estilos de formularios
    └── js/
        └── main.js               # JavaScript custom
```

---

## 👨‍💻 Guía para Desarrolladores

### Comandos Útiles

```bash
# Crear nuevas migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Acceder al shell de Django
python manage.py shell

# Resetear base de datos completa (¡CUIDADO!)
python manage.py seed --reset

# Ejecutar tests (cuando se implementen)
python manage.py test

# Recopilar archivos estáticos (producción)
python manage.py collectstatic
```

### Agregar Nueva Funcionalidad

#### 1. Crear nueva app

```bash
python manage.py startapp nombre_app
```

#### 2. Registrar en settings.py

```python
INSTALLED_APPS = [
    # ...
    'nombre_app',
]
```

#### 3. Crear modelos en models.py

```python
from django.db import models

class MiModelo(models.Model):
    nombre = models.CharField(max_length=100)
    # ...
```

#### 4. Crear migraciones y aplicarlas

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. Crear views en views.py

```python
from django.shortcuts import render
from .models import MiModelo

def mi_vista(request):
    objetos = MiModelo.objects.all()
    return render(request, 'mi_template.html', {'objetos': objetos})
```

#### 6. Configurar URLs en urls.py

```python
from django.urls import path
from . import views

app_name = 'nombre_app'

urlpatterns = [
    path('', views.mi_vista, name='listar'),
]
```

### Patrones de Código

#### Soft Delete en Modelos

```python
from django.db import models
from django.utils import timezone

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class MiModelo(models.Model):
    # ... campos ...
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = ActiveManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
```

#### Vista con Login Requerido

```python
from django.contrib.auth.decorators import login_required

@login_required
def mi_vista(request):
    # ... lógica ...
```

#### Vista solo para Admins

```python
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

@login_required
@user_passes_test(is_admin, login_url='clientes:listar')
def vista_admin(request):
    # ... lógica ...
```

---

## 📚 Documentación Técnica

Para información técnica detallada, consulta:

- **[AUDITORIA_TECNICA.md](AUDITORIA_TECNICA.md)** - Auditoría completa del backend y frontend
- **[QUICKSTART.md](QUICKSTART.md)** - Guía de inicio rápido
- **[Django Documentation](https://docs.djangoproject.com/en/4.2/)** - Documentación oficial de Django

### Contenido de AUDITORIA_TECNICA.md

- Arquitectura del sistema
- Detalles de cada aplicación Django
- Modelos con todos sus campos y relaciones
- Views con su lógica completa
- Formularios y validaciones
- Patrones de código utilizados
- Configuración crítica
- Análisis del frontend (templates, CSS, JavaScript)
- Dependencias y versiones
- Checklist pre-producción

---

## ❓ FAQ (Preguntas Frecuentes)

### ¿Por qué usar SQLite en lugar de PostgreSQL?

SQLite es perfecto para desarrollo y pruebas, pero **no se recomienda para producción**. Para producción, debes migrar a PostgreSQL o MySQL.

### ¿Cómo cambio la base de datos a PostgreSQL?

1. Instalar psycopg2: `pip install psycopg2-binary`
2. Modificar settings.py:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_bd',
        'USER': 'usuario',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### ¿Cómo agregar un nuevo tipo de usuario (rol)?

1. Acceder al admin de Django: http://localhost:8000/admin
2. Crear nuevo grupo en "Groups"
3. Asignar permisos al grupo
4. Al crear usuarios, asignarles ese grupo

### ¿El sistema envía emails reales?

Sí, si configuras las variables de entorno de email (EMAIL_HOST_USER, EMAIL_HOST_PASSWORD). En desarrollo, los emails se muestran en la consola.

### ¿Puedo usar esto en producción?

Sí, pero debes:

- Cambiar DEBUG=False
- Usar base de datos robusta (PostgreSQL)
- Configurar ALLOWED_HOSTS
- Usar servidor web (Gunicorn + Nginx)
- Configurar HTTPS
- Ver checklist en AUDITORIA_TECNICA.md

### ¿Cómo agrego más campos a Cliente o Mascota?

1. Editar `models.py` del app correspondiente
2. Agregar el campo: `nuevo_campo = models.CharField(max_length=100)`
3. Crear migración: `python manage.py makemigrations`
4. Aplicar: `python manage.py migrate`
5. Actualizar formulario en `forms.py`
6. Actualizar template HTML

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si quieres mejorar este proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Áreas donde puedes contribuir

- 📝 Agregar tests unitarios
- 🔄 Implementar paginación
- 📊 Crear dashboard con estadísticas
- 📅 Módulo de citas y agendamiento
- 💊 Módulo de inventario de medicamentos
- 📄 Historias clínicas detalladas
- 🌐 API REST (Django REST Framework)
- 📱 App móvil
- 🌍 Internacionalización (i18n)
- ♿ Mejorar accesibilidad (WCAG)

---

## 🐛 Reportar Bugs

Si encuentras un bug, por favor:

1. Verifica que no haya sido reportado ya
2. Crea un nuevo Issue en GitHub
3. Incluye:
   - Descripción clara del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Capturas de pantalla (si aplica)
   - Versión de Python y Django
   - Sistema operativo

---

## 📜 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

---

## 👥 Autores

- **Owner:** abarraza-v
- **Documentación:** GitHub Copilot

---

## 🙏 Agradecimientos

- Django Software Foundation por el increíble framework
- Bootstrap team por el framework CSS
- Comunidad de Python y Django

---

## 📞 Contacto

- **GitHub:** [@abarraza-v](https://github.com/abarraza-v)
- **Repositorio:** [sistema_veterinaria](https://github.com/abarraza-v/sistema_veterinaria)

---

## 🌟 Roadmap

### Versión 1.1 (Próxima)

- [ ] Implementar tests unitarios
- [ ] Paginación en listas
- [ ] Dashboard con estadísticas
- [ ] Exportar datos a Excel/PDF

### Versión 2.0

- [ ] Módulo de citas y agendamiento
- [ ] Historias clínicas completas
- [ ] Módulo de inventario
- [ ] API REST

### Versión 3.0

- [ ] Sistema de facturación
- [ ] App móvil
- [ ] Integración con servicios externos
- [ ] Reportes avanzados

---

**Última actualización:** 19 de diciembre de 2025  
**Versión del sistema:** 1.0  
**Framework:** Django 4.2.x

---

¿Te gustó el proyecto? ⭐ Dale una estrella en GitHub!
