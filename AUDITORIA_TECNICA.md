# Auditoría Técnica - Sistema Veterinaria "Patitas Felices"

## 📋 Resumen Ejecutivo

**Proyecto:** Sistema de Gestión Veterinaria  
**Framework:** Django 4.2.x  
**Tipo:** Aplicación Web Monolítica (Django Templates)  
**Base de Datos:** SQLite3 (desarrollo)  
**Arquitectura:** MVT (Model-View-Template) tradicional de Django  
**Estado:** Desarrollo/Producción temprana

---

## 🏗️ Estructura de Aplicaciones Django

### Tabla de Aplicaciones

| Aplicación        | Propósito                              | Modelos | Views | URLs | Forms |
| ----------------- | -------------------------------------- | ------- | ----- | ---- | ----- |
| **core**          | Utilidades compartidas y comandos      | 0       | 0     | 0    | 0     |
| **autenticacion** | Sistema de login y seguridad           | 2       | 2     | 8    | 1     |
| **clientes**      | Gestión de clientes                    | 1       | 5     | 5    | 1     |
| **mascotas**      | Gestión de mascotas                    | 1       | 5     | 5    | 1     |
| **usuarios**      | Administración de usuarios del sistema | 0       | 6     | 7    | 2     |

### Apps Instaladas (settings.py)

```python
INSTALLED_APPS = [
    'django.contrib.admin',        # Panel de administración
    'django.contrib.auth',         # Sistema de autenticación
    'django.contrib.contenttypes', # Sistema de tipos de contenido
    'django.contrib.sessions',     # Manejo de sesiones
    'django.contrib.messages',     # Sistema de mensajes
    'django.contrib.staticfiles',  # Archivos estáticos
    # Apps del proyecto
    'core',                        # Utilidades centrales
    'autenticacion',               # Login y seguridad
    'clientes',                    # Gestión de clientes
    'mascotas',                    # Gestión de mascotas
    'usuarios',                    # Gestión de usuarios
]
```

---

## 📦 Aplicaciones Principales

### 1. **CORE** - Aplicación de Utilidades

**Ubicación:** `core/`  
**Propósito:** Proveer utilidades compartidas, validadores y comandos de gestión

#### Archivos Principales

- **`utils.py`** - Funciones de validación y formato
- **`management/commands/seed.py`** - Comando para poblar BD con datos de prueba

#### Funciones Clave (utils.py)

| Función                                | Descripción                      | Parámetros      | Retorno             |
| -------------------------------------- | -------------------------------- | --------------- | ------------------- |
| `validar_rut(rut)`                     | Valida RUT chileno con Módulo 11 | String RUT      | Boolean             |
| `formatear_rut(rut)`                   | Formatea RUT a 12.345.678-9      | String RUT      | String formateado   |
| `limpiar_rut(rut)`                     | Elimina puntos y guiones         | String RUT      | String sin formato  |
| `validar_telefono_chileno(telefono)`   | Valida formato teléfono CL       | String teléfono | Boolean             |
| `formatear_telefono_chileno(telefono)` | Formatea a +56 9 8765 4321       | String teléfono | String formateado   |
| `limpiar_telefono(telefono)`           | Elimina caracteres no numéricos  | String teléfono | String solo números |

#### Management Commands

```bash
# Poblar base de datos con datos de prueba
python manage.py seed

# Resetear completamente la base de datos
python manage.py seed --reset
```

**Comando `seed`:**

- Crea 3 grupos de usuarios: Administrador, Recepcionista, Veterinario
- Genera 6 usuarios de prueba (1 admin, 2 recepcionistas [1 activo, 1 inactivo], 3 veterinarios)
- Crea 4 clientes de prueba
- Registra 6 mascotas de prueba
- Con `--reset`: elimina BD, migraciones, y recrea todo desde cero

#### Puntos de Integración

- Importado por: `clientes.forms`, `usuarios.forms`
- Usado para: validación de RUT y teléfonos en formularios

---

### 2. **AUTENTICACION** - Sistema de Login y Seguridad

**Ubicación:** `autenticacion/`  
**Propósito:** Manejo de autenticación, bloqueo de cuentas y recuperación de contraseñas

#### Modelos

##### `LoginAttempt`

**Propósito:** Rastrear intentos de login y bloquear cuentas por fuerza bruta

| Campo          | Tipo                  | Descripción                 |
| -------------- | --------------------- | --------------------------- |
| `username`     | CharField(150)        | Usuario que intenta acceder |
| `ip_address`   | GenericIPAddressField | IP desde donde se intenta   |
| `attempted_at` | DateTimeField         | Timestamp del intento       |
| `successful`   | BooleanField          | Si el intento fue exitoso   |

**Métodos de Clase:**

- `is_locked(username)` - Verifica si está bloqueado (5 intentos fallidos en 5 min)
- `get_remaining_attempts(username)` - Retorna intentos restantes antes del bloqueo
- `get_lockout_time_remaining(username)` - Segundos restantes de bloqueo

##### `UserProfile`

**Propósito:** Extender el modelo User con información adicional

| Campo                   | Tipo                | Descripción                           |
| ----------------------- | ------------------- | ------------------------------------- |
| `user`                  | OneToOneField(User) | Usuario relacionado                   |
| `debe_cambiar_password` | BooleanField        | Flag para forzar cambio de contraseña |
| `password_reset_date`   | DateTimeField       | Fecha del último reset                |

#### Views Principales

| View          | Método   | Propósito                                 |
| ------------- | -------- | ----------------------------------------- |
| `login_view`  | GET/POST | Login con validación de intentos fallidos |
| `logout_view` | GET      | Cierre de sesión                          |

**Flujo de Login:**

1. Verificar si usuario ya está autenticado
2. Validar que no esté bloqueado (LoginAttempt.is_locked)
3. Intentar autenticación (por username o email)
4. Registrar intento exitoso/fallido
5. Aplicar "recordar sesión" (session.set_expiry)
6. Verificar si debe cambiar contraseña (UserProfile)

#### URLs (8 endpoints)

```python
path('', views.login_view, name='login')
path('login/', views.login_view, name='login')
path('logout/', views.logout_view, name='logout')
path('password-reset/', PasswordResetView, name='password_reset')
path('password-reset/done/', PasswordResetDoneView, name='password_reset_done')
path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView)
path('password-reset-complete/', PasswordResetCompleteView)
```

#### Formularios

**`LoginForm`**

- Campos: username, password, remember_me
- Validación de bloqueo de cuenta (5 intentos fallidos)
- Autenticación por username o email
- Registro de IP del cliente
- Contador de intentos restantes en mensajes de error

#### Seguridad Implementada

- ✅ Bloqueo temporal por 5 minutos tras 5 intentos fallidos
- ✅ Registro de intentos con IP
- ✅ Autenticación por email o username
- ✅ Validación de usuarios inactivos
- ✅ Forzar cambio de contraseña al primer login
- ✅ Sistema de recuperación de contraseña por email

#### Plantillas

- `login.html` - Formulario de login
- `password_reset_form.html` - Solicitar reset
- `password_reset_email.html` - Email con link
- `password_reset_done.html` - Confirmación de envío
- `password_reset_confirm.html` - Establecer nueva contraseña
- `password_reset_complete.html` - Confirmación final

---

### 3. **CLIENTES** - Gestión de Clientes

**Ubicación:** `clientes/`  
**Propósito:** CRUD de clientes con soft delete

#### Modelos

##### `Cliente`

**Propósito:** Representar a los dueños de mascotas

| Campo        | Tipo           | Restricciones    | Descripción              |
| ------------ | -------------- | ---------------- | ------------------------ |
| `nombre`     | CharField(200) | Required         | Nombre completo          |
| `rut`        | CharField(12)  | Unique           | RUT chileno              |
| `telefono`   | CharField(15)  | Required         | Teléfono formato CL      |
| `email`      | EmailField     | Optional, Unique | Correo electrónico       |
| `is_deleted` | BooleanField   | Default: False   | Soft delete flag         |
| `deleted_at` | DateTimeField  | Nullable         | Timestamp de eliminación |
| `created_at` | DateTimeField  | Auto             | Fecha de creación        |
| `updated_at` | DateTimeField  | Auto             | Última actualización     |

**Custom Manager:**

- `objects` - ActiveManager (filtra is_deleted=False)
- `all_objects` - Manager estándar (incluye eliminados)

**Métodos:**

- `soft_delete()` - Marca como eliminado sin borrar el registro
- `restore()` - Restaura un cliente eliminado

**Relaciones:**

- `mascotas` (ForeignKey reverso) - Mascotas del cliente

#### Views

| View       | Decorador       | Propósito                                           |
| ---------- | --------------- | --------------------------------------------------- |
| `listar`   | @login_required | Vista unificada de clientes y mascotas con pestañas |
| `crear`    | @login_required | Formulario de creación de cliente                   |
| `editar`   | @login_required | Formulario de edición de cliente                    |
| `eliminar` | @login_required | Soft delete (solo admins)                           |
| `detalle`  | @login_required | Vista detallada con mascotas asociadas              |

**Vista `listar` - Características especiales:**

- Switch entre pestañas "Clientes" y "Mascotas"
- Búsqueda por: nombre, RUT, teléfono, email (clientes)
- Búsqueda por: nombre mascota, dueño, especie, raza (mascotas)
- Conteo de mascotas activas por cliente (annotation)
- Soporte AJAX para modales

#### Formularios

**`ClienteForm`**

- Validación de RUT con algoritmo Módulo 11
- Formateo automático de RUT (12.345.678-9)
- Validación de teléfono chileno
- Formateo automático de teléfono (+56 9 8765 4321)
- Verificación de unicidad de RUT y email
- Validaciones:
  - Nombre mínimo 3 caracteres
  - Nombre no puede ser solo números
  - Teléfono mínimo 8 dígitos
  - RUT único en sistema

#### URLs (5 endpoints)

```python
path('', views.listar, name='listar')
path('crear/', views.crear, name='crear')
path('editar/<int:pk>/', views.editar, name='editar')
path('eliminar/<int:pk>/', views.eliminar, name='eliminar')
path('detalle/<int:pk>/', views.detalle, name='detalle')
```

#### Reglas de Negocio

- Solo administradores pueden eliminar clientes
- No se puede eliminar un cliente con mascotas activas
- El email es opcional pero si se proporciona debe ser único
- RUT y teléfono se formatean automáticamente al guardar

#### Plantillas

- `clientes_mascotas.html` - Vista unificada con tabs
- `cliente_form.html` - Formulario crear/editar
- `cliente_confirm_delete.html` - Confirmación de eliminación
- `cliente_detalle_modal.html` - Modal de detalles (AJAX)

---

### 4. **MASCOTAS** - Gestión de Mascotas

**Ubicación:** `mascotas/`  
**Propósito:** CRUD de mascotas con soft delete

#### Modelos

##### `Mascota`

**Propósito:** Representar a los pacientes de la veterinaria

| Campo              | Tipo                | Restricciones     | Descripción                            |
| ------------------ | ------------------- | ----------------- | -------------------------------------- |
| `dueno`            | ForeignKey(Cliente) | Required, CASCADE | Dueño de la mascota                    |
| `nombre`           | CharField(100)      | Required          | Nombre de la mascota                   |
| `especie`          | CharField(50)       | Choices           | Perro, Gato, Ave, Roedor, Reptil, Otro |
| `especie_otro`     | CharField(50)       | Optional          | Si especie es "Otro"                   |
| `raza`             | CharField(100)      | Required          | Raza de la mascota                     |
| `sexo`             | CharField(10)       | Choices           | Macho, Hembra                          |
| `edad`             | DecimalField(5,1)   | Optional          | Edad en años (auto-calculada)          |
| `fecha_nacimiento` | DateField           | Optional          | Fecha de nacimiento                    |
| `alergias`         | TextField           | Optional          | Alergias conocidas                     |
| `is_deleted`       | BooleanField        | Default: False    | Soft delete flag                       |
| `deleted_at`       | DateTimeField       | Nullable          | Timestamp eliminación                  |
| `created_at`       | DateTimeField       | Auto              | Fecha de creación                      |
| `updated_at`       | DateTimeField       | Auto              | Última actualización                   |

**Choices:**

```python
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
```

**Custom Manager:**

- `objects` - ActiveManager (filtra is_deleted=False)
- `all_objects` - Manager estándar (incluye eliminados)

**Métodos:**

- `soft_delete()` - Marca como eliminada
- `restore()` - Restaura mascota eliminada
- `get_especie_display_custom()` - Retorna especie, usando especie_otro si aplica

**Relaciones:**

- `dueno` → Cliente (Many-to-One)

#### Views

| View       | Decorador       | Propósito                               |
| ---------- | --------------- | --------------------------------------- |
| `listar`   | @login_required | Redirige a clientes:listar?tab=mascotas |
| `crear`    | @login_required | Formulario de creación de mascota       |
| `editar`   | @login_required | Formulario de edición de mascota        |
| `eliminar` | @login_required | Soft delete (solo admins)               |
| `detalle`  | @login_required | Vista detallada de mascota              |

#### Formularios

**`MascotaForm`**

- Dropdown de dueños filtrado (solo clientes activos)
- Campo "especie_otro" se muestra solo si especie == "Otro" (JavaScript)
- Cálculo automático de edad basado en fecha_nacimiento (JavaScript)
- Validaciones:
  - Nombre mínimo 2 caracteres
  - Fecha nacimiento no puede ser futura
  - Edad máxima 30 años (validación de fecha razonable)
  - Si especie es "Otro", campo especie_otro es requerido
  - Nombre no puede ser solo números

**Lógica de Edad:**

- Si se proporciona fecha_nacimiento, edad se calcula automáticamente (readonly)
- Si no hay fecha_nacimiento, edad se puede ingresar manualmente

#### URLs (5 endpoints)

```python
path('', views.listar, name='listar')
path('crear/', views.crear, name='crear')
path('editar/<int:pk>/', views.editar, name='editar')
path('eliminar/<int:pk>/', views.eliminar, name='eliminar')
path('detalle/<int:pk>/', views.detalle, name='detalle')
```

#### Reglas de Negocio

- Solo administradores pueden eliminar mascotas
- Una mascota debe tener un dueño activo
- Si especie es "Otro", debe especificar en especie_otro
- Edad se calcula automáticamente si hay fecha de nacimiento

#### Plantillas

- `mascota_form.html` - Formulario crear/editar
- `mascota_confirm_delete.html` - Confirmación de eliminación
- `mascota_detalle_modal.html` - Modal de detalles (AJAX)

---

### 5. **USUARIOS** - Gestión de Usuarios del Sistema

**Ubicación:** `usuarios/`  
**Propósito:** CRUD de usuarios, asignación de roles, reset de contraseñas

#### Modelos

No tiene modelos propios, usa el modelo `User` de Django y `UserProfile` de autenticacion.

#### Views

| View               | Decorador                                     | Propósito                  |
| ------------------ | --------------------------------------------- | -------------------------- |
| `listar`           | @login_required + @user_passes_test(is_admin) | Lista usuarios del sistema |
| `crear`            | @login_required + @user_passes_test(is_admin) | Crear nuevo usuario        |
| `editar`           | @login_required + @user_passes_test(is_admin) | Editar usuario existente   |
| `toggle_active`    | @login_required + @user_passes_test(is_admin) | Activar/Desactivar usuario |
| `reset_password`   | @login_required + @user_passes_test(is_admin) | Resetear contraseña        |
| `cambiar_password` | @login_required                               | Cambiar propia contraseña  |
| `detalle`          | @login_required + @user_passes_test(is_admin) | Ver detalles de usuario    |

**Helper Functions:**

- `is_admin(user)` - Verifica si usuario pertenece al grupo "Administrador"
- `generar_password(length=12)` - Genera contraseña aleatoria segura
- `enviar_credenciales(usuario, password)` - Envía email con credenciales
- `enviar_nueva_password(usuario, password)` - Envía email con nueva contraseña

#### Formularios

**`UsuarioForm`**

- Campos: first_name, last_name, email, grupo (rol)
- Genera username automáticamente desde email
- Genera contraseña aleatoria en creación
- Asigna usuario al grupo seleccionado
- Marca "debe_cambiar_password" en UserProfile
- Validaciones:
  - Email único en sistema
  - Nombre y apellido mínimo 2 caracteres
  - No pueden ser solo números

**Flujo de Creación:**

1. Admin llena formulario con nombre, email y rol
2. Sistema genera username desde email (ej: juan@email.cl → juan)
3. Sistema genera contraseña aleatoria de 12 caracteres
4. Se crea UserProfile con flag debe_cambiar_password=True
5. Se envía email con credenciales al nuevo usuario
6. Usuario debe cambiar contraseña en primer login

#### URLs (7 endpoints)

```python
path('', views.listar, name='listar')
path('crear/', views.crear, name='crear')
path('editar/<int:pk>/', views.editar, name='editar')
path('toggle/<int:pk>/', views.toggle_active, name='toggle_active')
path('reset_password/<int:pk>/', views.reset_password, name='reset_password')
path('cambiar_password/<int:pk>/', views.cambiar_password, name='cambiar_password')
path('detalle/<int:pk>/', views.detalle, name='detalle')
```

#### Roles de Usuario (Grupos Django)

| Grupo             | Permisos                                                    |
| ----------------- | ----------------------------------------------------------- |
| **Administrador** | Acceso total, gestión de usuarios, eliminación de registros |
| **Recepcionista** | Ver, crear y editar clientes/mascotas, no eliminar          |
| **Veterinario**   | Ver, crear y editar clientes/mascotas, no eliminar          |

#### Reglas de Negocio

- Solo administradores acceden a esta app
- No se puede editar el primer usuario del sistema (superusuario original)
- No se puede editar el propio usuario (evitar auto-bloqueo)
- No se puede desactivar el propio usuario
- Reset de contraseña fuerza cambio en siguiente login
- Usuarios inactivos no pueden iniciar sesión

#### Plantillas

- `usuario_list.html` - Lista de usuarios
- `usuario_form.html` - Formulario crear/editar
- `usuario_toggle_confirm.html` - Confirmar activar/desactivar
- `usuario_reset_password_confirm.html` - Confirmar reset de contraseña
- `cambiar_password.html` - Formulario cambio de contraseña
- `usuario_detalle_modal.html` - Modal de detalles (AJAX)

---

## ⚙️ Patrones Transversales

### Custom Managers

**`ActiveManager`** (usado en Cliente y Mascota)

```python
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
```

- **Propósito:** Filtrar automáticamente registros eliminados (soft delete)
- **Uso:** `Cliente.objects.all()` excluye is_deleted=True
- **Acceso a eliminados:** `Cliente.all_objects.all()`

### Soft Delete Pattern

Implementado en: Cliente, Mascota

**Campos:**

- `is_deleted` (BooleanField) - Flag de eliminación
- `deleted_at` (DateTimeField) - Timestamp de eliminación

**Métodos:**

```python
def soft_delete(self):
    self.is_deleted = True
    self.deleted_at = timezone.now()
    self.save()

def restore(self):
    self.is_deleted = False
    self.deleted_at = None
    self.save()
```

**Ventajas:**

- Auditoría completa (nunca se pierde información)
- Posibilidad de restaurar registros
- Cumplimiento normativo (trazabilidad)

### Validadores Custom

#### Validación de RUT (Módulo 11)

**Ubicación:** `core/utils.py`
**Algoritmo:**

1. Limpiar formato (eliminar puntos y guiones)
2. Separar número y dígito verificador
3. Aplicar multiplicadores 2-7 en reversa
4. Calcular módulo 11
5. Comparar dígito verificador

#### Validación de Teléfono Chileno

**Ubicación:** `core/utils.py`
**Reglas:**

- Debe tener entre 8 y 11 dígitos
- Formato con código país: +56 9 8765 4321
- Soporta fijos y móviles

### Decoradores de Permisos

```python
@login_required
@user_passes_test(is_admin, login_url='clientes:listar')
def vista_solo_admin(request):
    # Solo usuarios del grupo "Administrador" pueden acceder
```

**Decoradores usados:**

- `@login_required` - Requiere autenticación
- `@user_passes_test(is_admin)` - Requiere ser administrador
- `@require_http_methods(["GET", "POST"])` - Restringe métodos HTTP

### Mensajes Flash

**Sistema de mensajes de Django:**

```python
messages.success(request, 'Operación exitosa')
messages.error(request, 'Error en operación')
messages.warning(request, 'Advertencia')
messages.info(request, 'Información')
```

**Auto-dismiss:** JavaScript cierra mensajes después de 5 segundos

---

## 🔐 Configuración Crítica

### Settings.py

#### Seguridad

```python
SECRET_KEY = config('SECRET_KEY', default='...')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
```

#### Base de Datos (Desarrollo)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Nota:** SQLite solo para desarrollo. Producción debería usar PostgreSQL o MySQL.

#### Internacionalización

```python
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True
```

#### Autenticación

```python
LOGIN_URL = 'autenticacion:login'
LOGIN_REDIRECT_URL = 'clientes:listar'
LOGOUT_REDIRECT_URL = 'autenticacion:login'
```

#### Email (SMTP)

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
```

#### Archivos Estáticos

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

#### Middleware Stack

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',       # Seguridad
    'django.contrib.sessions.middleware.SessionMiddleware', # Sesiones
    'django.middleware.common.CommonMiddleware',           # Headers comunes
    'django.middleware.csrf.CsrfViewMiddleware',           # Protección CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Autenticación
    'django.contrib.messages.middleware.MessageMiddleware', # Mensajes
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Anti-clickjacking
]
```

**Nota:** No hay middleware custom implementado.

### Variables de Entorno Necesarias

**Archivo:** `.env` (no versionado)

```ini
# Seguridad
SECRET_KEY=tu-secret-key-super-segura-aqui
DEBUG=True

# Hosts permitidos (separados por coma)
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (para recuperación de contraseña)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
```

**Herramienta de config:** python-decouple

### Configuración por Entorno

| Entorno        | DEBUG | DB         | ALLOWED_HOSTS       | EMAIL           |
| -------------- | ----- | ---------- | ------------------- | --------------- |
| **Desarrollo** | True  | SQLite     | localhost           | Console backend |
| **Staging**    | False | PostgreSQL | staging.example.com | SMTP            |
| **Producción** | False | PostgreSQL | veterinaria.cl      | SMTP            |

---

## 📚 Dependencias Críticas

### requirements.txt

| Paquete             | Versión    | Propósito                          |
| ------------------- | ---------- | ---------------------------------- |
| **Django**          | >=4.2,<5.0 | Framework principal                |
| **python-decouple** | >=3.8      | Gestión de variables de entorno    |
| **python-dotenv**   | >=1.0.0    | Carga de archivos .env             |
| **Pillow**          | >=10.0.0   | Procesamiento de imágenes (futuro) |

### Librerías Frontend (CDN)

| Librería            | Versión | Propósito     |
| ------------------- | ------- | ------------- |
| **Bootstrap**       | 5.3.0   | Framework CSS |
| **Bootstrap Icons** | 1.11.0  | Iconos        |

---

## 🎨 Frontend - Análisis Detallado

### Arquitectura Frontend

**Tipo:** Server-Side Rendering (SSR) con Django Templates  
**Framework CSS:** Bootstrap 5.3  
**JavaScript:** Vanilla JS (sin frameworks)  
**Patrón:** Template Inheritance (Django)

### Estructura de Templates

```
templates/
├── base.html                   # Template base (HTML, links CSS/JS)
├── base_with_sidebar.html      # Extiende base, agrega sidebar de navegación
│
├── autenticacion/
│   ├── login.html              # Formulario de login
│   └── password_reset_*.html   # Flujo de recuperación de contraseña
│
├── clientes/
│   ├── clientes_mascotas.html  # Vista unificada con tabs
│   ├── cliente_form.html       # Formulario crear/editar
│   ├── cliente_confirm_delete.html
│   └── cliente_detalle_modal.html
│
├── mascotas/
│   ├── mascota_form.html
│   ├── mascota_confirm_delete.html
│   └── mascota_detalle_modal.html
│
└── usuarios/
    ├── usuario_list.html
    ├── usuario_form.html
    ├── cambiar_password.html
    ├── usuario_toggle_confirm.html
    ├── usuario_reset_password_confirm.html
    └── usuario_detalle_modal.html
```

### Template Inheritance

**Jerarquía:**

```
base.html
  └── base_with_sidebar.html
        ├── clientes_mascotas.html
        ├── usuario_list.html
        └── otras vistas del sistema
```

**base.html** (raíz):

- Define estructura HTML básica
- Carga Bootstrap CSS/JS
- Carga CSS y JS custom
- Bloques: `{% block title %}`, `{% block content %}`, `{% block extra_css %}`, `{% block extra_js %}`

**base_with_sidebar.html** (extendido):

- Agrega sidebar de navegación
- Sistema de mensajes flash
- Información de usuario logueado
- Reloj en tiempo real
- Bloque: `{% block main_content %}`

### Archivos Estáticos

#### CSS Personalizado

**Ubicación:** `static/css/`

| Archivo         | Propósito                            |
| --------------- | ------------------------------------ |
| **main.css**    | Estilos generales de la aplicación   |
| **sidebar.css** | Estilos del sidebar de navegación    |
| **forms.css**   | Estilos específicos para formularios |

**Principales estilos:**

- Sistema de colores consistente
- Responsividad mobile-first
- Animaciones sutiles (fade-in, hover effects)
- Cards y modales estilizados
- Badges de estado (activo/inactivo)

#### JavaScript Custom

**Ubicación:** `static/js/main.js`

**Funcionalidades implementadas:**

1. **Formateo de RUT en tiempo real**

   ```javascript
   function formatRUT(input)
   // Formatea mientras el usuario escribe: 12.345.678-9
   ```

2. **Formateo de Teléfono en tiempo real**

   ```javascript
   function formatPhone(input)
   // Formatea a: +56 9 8765 4321
   ```

3. **Mostrar/Ocultar campo "especie_otro"**

   ```javascript
   // Si especie == "Otro", muestra campo de texto adicional
   ```

4. **Cálculo automático de edad**

   ```javascript
   // Calcula edad basada en fecha_nacimiento
   ```

5. **Auto-dismiss de mensajes**

   ```javascript
   // Cierra alerts después de 5 segundos
   ```

6. **Toggle sidebar en móvil**

   ```javascript
   // Hamburger menu para responsive
   ```

7. **Confirmación de eliminación**
   ```javascript
   function confirmDelete(message)
   ```

### Componentes UI

#### Sidebar de Navegación

**Elementos:**

- Logo y nombre de la veterinaria
- Reloj en tiempo real (actualizado cada minuto)
- Avatar y nombre del usuario logueado
- Rol del usuario (grupo)
- Links de navegación con iconos
- Botón de cerrar sesión

**Links condicionales:**

```django
{% if request.user.groups.first.name == 'Administrador' %}
    <a href="{% url 'usuarios:listar' %}">
        <i class="bi bi-person-gear"></i> Gestión de Usuarios
    </a>
{% endif %}
```

**Responsive:**

- Desktop: Sidebar fijo a la izquierda (250px)
- Mobile: Sidebar colapsable con botón hamburger

#### Sistema de Pestañas (Tabs)

**Ubicación:** clientes_mascotas.html

```html
<ul class="nav nav-tabs">
  <li class="nav-item">
    <a
      class="nav-link {% if tab == 'clientes' %}active{% endif %}"
      href="?tab=clientes"
      >Clientes</a
    >
  </li>
  <li class="nav-item">
    <a
      class="nav-link {% if tab == 'mascotas' %}active{% endif %}"
      href="?tab=mascotas"
      >Mascotas</a
    >
  </li>
</ul>
```

**Estado persistente:** Parámetro GET `?tab=clientes` o `?tab=mascotas`

#### Modales AJAX

**Implementación:**

```javascript
// Request AJAX con header
fetch(url, {
  headers: {
    "X-Requested-With": "XMLHttpRequest",
  },
});
```

**Backend detecta AJAX:**

```python
if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    return render(request, 'template_modal.html', context)
```

**Modales implementados:**

- Ver detalles de cliente
- Ver detalles de mascota
- Ver detalles de usuario

#### Formularios

**Características:**

- Bootstrap 5 form controls
- Validación HTML5
- Validación custom en JavaScript
- Formateo automático de campos (RUT, teléfono)
- Campos condicionales (especie_otro)
- Mensajes de error claros
- Botones de acción con iconos

**Ejemplo de campo:**

```django
<div class="mb-3">
    <label for="id_rut" class="form-label">RUT</label>
    {{ form.rut }}
    {% if form.rut.errors %}
        <div class="invalid-feedback d-block">
            {{ form.rut.errors.0 }}
        </div>
    {% endif %}
</div>
```

#### Tablas de Datos

**Características:**

- Responsive (scroll horizontal en móvil)
- Hover effects
- Badges de estado
- Botones de acción (editar, eliminar, ver)
- Filas alternadas
- Contadores (ej: número de mascotas)

**Ejemplo:**

```html
<table class="table table-hover">
  <thead>
    <tr>
      <th>Nombre</th>
      <th>RUT</th>
      <th>Mascotas</th>
      <th>Acciones</th>
    </tr>
  </thead>
  <tbody>
    {% for cliente in clientes %}
    <tr>
      <td>{{ cliente.nombre }}</td>
      <td>{{ cliente.rut }}</td>
      <td><span class="badge bg-info">{{ cliente.num_mascotas }}</span></td>
      <td>
        <a
          href="{% url 'clientes:editar' cliente.pk %}"
          class="btn btn-sm btn-primary"
        >
          <i class="bi bi-pencil"></i>
        </a>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
```

#### Sistema de Búsqueda

**Características:**

- Barra de búsqueda en tiempo real
- Búsqueda por múltiples campos (Q objects)
- Icono de búsqueda (Bootstrap Icons)
- Placeholder descriptivo
- Preserva query en redirecciones

**Implementación:**

```html
<form method="GET" class="mb-4">
  <div class="input-group">
    <span class="input-group-text"><i class="bi bi-search"></i></span>
    <input
      type="text"
      name="q"
      class="form-control"
      placeholder="Buscar por nombre, RUT, teléfono o email..."
      value="{{ query }}"
    />
    <button class="btn btn-primary" type="submit">Buscar</button>
  </div>
</form>
```

#### Badges de Estado

**Tipos:**

- **Activo:** `<span class="badge bg-success">Activo</span>`
- **Inactivo:** `<span class="badge bg-danger">Inactivo</span>`
- **Contador:** `<span class="badge bg-info">5</span>`
- **Rol:** `<span class="badge bg-primary">Administrador</span>`

### UX/UI Patterns

#### Confirmaciones de Eliminación

**Flujo:**

1. Usuario hace clic en botón "Eliminar"
2. Redirección a página de confirmación
3. Muestra información del registro a eliminar
4. Advertencias si hay relaciones (ej: cliente con mascotas)
5. Botones: "Cancelar" (gris) y "Eliminar" (rojo)

#### Mensajes Flash

**Tipos:**

- `success` - Verde con ícono check
- `error` - Rojo con ícono alerta
- `warning` - Amarillo con ícono advertencia
- `info` - Azul con ícono info

**Auto-dismiss:** 5 segundos (JavaScript)

#### Breadcrumbs

**Ejemplo:**

```html
<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="/">Inicio</a></li>
    <li class="breadcrumb-item active">Clientes</li>
  </ol>
</nav>
```

#### Paginación

**Nota:** Actualmente no implementada. Para datasets grandes, se recomienda:

```python
from django.core.paginator import Paginator

paginator = Paginator(clientes, 25)  # 25 por página
page_obj = paginator.get_page(request.GET.get('page'))
```

### Responsive Design

**Breakpoints (Bootstrap 5):**

- xs: < 576px (móvil)
- sm: ≥ 576px (móvil grande)
- md: ≥ 768px (tablet)
- lg: ≥ 992px (desktop)
- xl: ≥ 1200px (desktop grande)

**Adaptaciones:**

- Sidebar colapsa en móvil
- Tablas con scroll horizontal
- Formularios apilados en móvil
- Botones full-width en móvil
- Cards en grid responsive

### Accesibilidad (A11y)

**Características implementadas:**

- Etiquetas `<label>` asociadas a inputs
- Atributos ARIA cuando necesario
- Contraste de colores suficiente
- Focus visible en elementos interactivos
- Mensajes de error descriptivos

**Áreas de mejora:**

- Añadir navegación por teclado completa
- Mejorar ARIA labels en botones de acción
- Implementar skip links
- Añadir live regions para cambios dinámicos

### Performance Frontend

**Optimizaciones:**

- CSS/JS cargados desde CDN (caching)
- Archivos CSS custom minificados (en producción)
- JavaScript sin dependencias pesadas
- Imágenes optimizadas (cuando se usen)
- No hay Single Page App (SPA) overhead

**Métricas estimadas:**

- First Contentful Paint: < 1.5s
- Time to Interactive: < 2.5s
- Total Blocking Time: < 200ms

---

## 🔍 Análisis de Integración

### Dependencias entre Apps

```
core
 ↓
 └──> clientes ──→ mascotas
        ↓             ↓
        └──────┬──────┘
               ↓
         autenticacion ←── usuarios
```

**Explicación:**

- **core** → Provee utilidades a todas las apps (sin dependencias)
- **clientes** → Usa core.utils para validación
- **mascotas** → Depende de Cliente (ForeignKey)
- **autenticacion** → Usa User de Django, provee LoginAttempt y UserProfile
- **usuarios** → Usa autenticacion.models (UserProfile)

### Flujo de Datos Principal

1. **Usuario se autentica** (autenticacion)
2. **Navega a Clientes** (clientes)
3. **Crea/edita Cliente** (clientes + core.utils)
4. **Registra Mascota** (mascotas + clientes)
5. **Admin gestiona usuarios** (usuarios + autenticacion)

---

## 📊 Modelo de Datos Completo

### Diagrama ER (Textual)

```
┌─────────────────┐
│  User (Django)  │
├─────────────────┤
│ id (PK)         │
│ username        │
│ email           │
│ first_name      │
│ last_name       │
│ is_active       │
│ is_staff        │
│ is_superuser    │
└────────┬────────┘
         │ 1:1
         ↓
┌─────────────────┐        ┌──────────────────┐
│  UserProfile    │        │  LoginAttempt    │
├─────────────────┤        ├──────────────────┤
│ id (PK)         │        │ id (PK)          │
│ user_id (FK)    │        │ username         │
│ debe_cambiar_pw │        │ ip_address       │
│ password_reset  │        │ attempted_at     │
└─────────────────┘        │ successful       │
                           └──────────────────┘

┌─────────────────┐
│    Cliente      │
├─────────────────┤
│ id (PK)         │
│ nombre          │
│ rut (UNIQUE)    │
│ telefono        │
│ email           │
│ is_deleted      │
│ deleted_at      │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │ 1:N
         ↓
┌─────────────────┐
│    Mascota      │
├─────────────────┤
│ id (PK)         │
│ dueno_id (FK)   │
│ nombre          │
│ especie         │
│ especie_otro    │
│ raza            │
│ sexo            │
│ edad            │
│ fecha_nac       │
│ alergias        │
│ is_deleted      │
│ deleted_at      │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### Índices y Optimizaciones

**Índices automáticos (Django):**

- PRIMARY KEY en todos los modelos
- UNIQUE en Cliente.rut
- FOREIGN KEY en Mascota.dueno_id, UserProfile.user_id

**Índices recomendados (no implementados):**

```python
# En Cliente
class Meta:
    indexes = [
        models.Index(fields=['nombre']),
        models.Index(fields=['rut']),
        models.Index(fields=['email']),
    ]

# En Mascota
class Meta:
    indexes = [
        models.Index(fields=['nombre']),
        models.Index(fields=['especie']),
    ]
```

---

## 🚀 Despliegue y Configuración

### Comandos Principales

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Activar entorno (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Poblar base de datos
python manage.py seed

# Resetear BD completa
python manage.py seed --reset

# Ejecutar servidor de desarrollo
python manage.py runserver

# Recopilar archivos estáticos (producción)
python manage.py collectstatic
```

### Checklist Pre-Producción

#### Seguridad

- [ ] SECRET_KEY único y seguro (no el default)
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS configurado correctamente
- [ ] HTTPS habilitado
- [ ] SECURE_SSL_REDIRECT = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True
- [ ] SECURE_BROWSER_XSS_FILTER = True
- [ ] X_FRAME_OPTIONS = 'DENY'

#### Base de Datos

- [ ] Migrar de SQLite a PostgreSQL/MySQL
- [ ] Backups automáticos configurados
- [ ] Índices de base de datos creados
- [ ] Configurar connection pooling

#### Email

- [ ] Servicio SMTP configurado (Gmail, SendGrid, etc.)
- [ ] Templates de email personalizados
- [ ] Dominio verificado (SPF, DKIM)

#### Performance

- [ ] Static files en CDN o servidor dedicado
- [ ] Caching configurado (Redis/Memcached)
- [ ] Compression habilitado (gzip)
- [ ] Logs configurados (Sentry para errores)

#### Funcionalidad

- [ ] Todos los tests pasando
- [ ] Validación de formularios exhaustiva
- [ ] Manejo de errores 404, 500
- [ ] Paginación en listas grandes

---

## 📝 Notas Técnicas

### Limitaciones Actuales

1. **Base de Datos:** SQLite no es adecuado para producción (no soporta concurrencia)
2. **Sin Paginación:** Listas pueden ser lentas con muchos registros
3. **Sin Tests Unitarios:** No hay suite de tests implementada
4. **Sin API REST:** No hay endpoints JSON (solo HTML)
5. **Sin Citas/Consultas:** Sistema básico, falta módulo de agendamiento
6. **Sin Inventario:** No hay módulo de productos/medicamentos
7. **Sin Facturación:** No hay módulo financiero

### Áreas de Mejora

#### Corto Plazo

- Implementar paginación en listas
- Añadir tests unitarios
- Migrar a PostgreSQL
- Mejorar manejo de errores

#### Mediano Plazo

- Crear API REST (Django REST Framework)
- Módulo de citas y agendamiento
- Sistema de roles más granular (permisos por objeto)
- Dashboard con estadísticas

#### Largo Plazo

- Módulo de inventario
- Sistema de facturación
- Historias clínicas completas
- App móvil (consumiendo API)

### Buenas Prácticas Implementadas

✅ Soft delete para auditoría  
✅ Custom managers para filtrado automático  
✅ Validación de RUT chileno  
✅ Bloqueo de cuentas por intentos fallidos  
✅ Generación segura de contraseñas  
✅ Separación de entornos con .env  
✅ Template inheritance  
✅ Decoradores de permisos  
✅ Mensajes flash para feedback  
✅ Formularios con validación robusta

---

## 🔗 Recursos Adicionales

### Documentación Relevante

- [Django 4.2 Documentation](https://docs.djangoproject.com/en/4.2/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)
- [Django Authentication System](https://docs.djangoproject.com/en/4.2/topics/auth/)
- [Django Forms API](https://docs.djangoproject.com/en/4.2/ref/forms/api/)

### Archivos Clave para Desarrolladores

| Archivo                           | Propósito               |
| --------------------------------- | ----------------------- |
| `sistema_veterinaria/settings.py` | Configuración principal |
| `sistema_veterinaria/urls.py`     | Routing principal       |
| `core/utils.py`                   | Utilidades compartidas  |
| `requirements.txt`                | Dependencias Python     |
| `QUICKSTART.md`                   | Guía de inicio rápido   |
| `manage.py`                       | CLI de Django           |

---

## 📞 Soporte y Mantenimiento

### Contacto Técnico

- **Repositorio:** sistema_veterinaria
- **Rama principal:** develop
- **Owner:** abarraza-v

### Control de Versiones

- **Git:** Repositorio activo
- **Rama de desarrollo:** develop
- **Convención de commits:** Descriptivos en español

---

**Documento generado:** 19 de diciembre de 2025  
**Auditor:** GitHub Copilot  
**Versión del sistema:** 1.0  
**Framework:** Django 4.2.x
