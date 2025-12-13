# Sistema de Gestión Veterinaria "Patitas Felices"

Sistema completo de gestión para veterinarias desarrollado con Django, utilizando arquitectura MVT (Model-View-Template), vistas basadas en funciones (FBV), Bootstrap 5 para estilos, y SQLite como base de datos.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)

## 📋 Características Principales

### Autenticación y Seguridad
- ✅ Sistema de login con autenticación de usuarios
- ✅ Sistema de bloqueo temporal: 5 intentos fallidos = bloqueo de 5 minutos
- ✅ Roles de usuario (Administrador, Recepcionista, Veterinario)
- ✅ Protección de vistas según permisos

### Gestión de Clientes
- ✅ CRUD completo de clientes
- ✅ Validación y formato automático de RUT chileno
- ✅ Formato automático de teléfonos chilenos
- ✅ Búsqueda por nombre, RUT o teléfono
- ✅ Soft delete (solo administradores)

### Gestión de Mascotas
- ✅ CRUD completo de mascotas
- ✅ Asociación con clientes
- ✅ Múltiples especies (Perro, Gato, Ave, Roedor, Reptil, Otro)
- ✅ Gestión de información médica (alergias, edad, fecha de nacimiento)
- ✅ Búsqueda por nombre, dueño o especie
- ✅ Soft delete (solo administradores)

### Gestión de Usuarios (Solo Administradores)
- ✅ CRUD completo de usuarios del sistema
- ✅ Generación automática de contraseñas
- ✅ Envío de credenciales por email
- ✅ Activación/desactivación de usuarios
- ✅ Restablecimiento de contraseñas

### Interfaz de Usuario
- ✅ Diseño responsive con Bootstrap 5
- ✅ Sidebar persistente con navegación
- ✅ Vista unificada de Clientes y Mascotas con switch de pestañas
- ✅ Cards informativos y tablas modernas
- ✅ Mensajes de confirmación y alertas

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd sistema_veterinaria
```

2. **Crear y activar entorno virtual**

En Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

En Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

Copiar el archivo `.env.example` a `.env` y configurar:
```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:
```env
SECRET_KEY=tu-secret-key-segura-aqui
DEBUG=True

# Email settings (opcional, para envío de credenciales)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
```

5. **Aplicar migraciones**
```bash
python manage.py migrate
```

6. **Cargar datos de prueba**
```bash
python manage.py seed
```

Este comando creará:
- Grupos de usuarios (Administrador, Recepcionista, Veterinario)
- Usuarios de prueba con credenciales
- Clientes de ejemplo
- Mascotas de ejemplo

7. **Ejecutar el servidor**
```bash
python manage.py runserver
```

8. **Acceder al sistema**
Abrir el navegador en: `http://localhost:8000`

## 👤 Usuarios de Prueba

Después de ejecutar `python manage.py seed`, tendrás los siguientes usuarios:

| Rol | Email | Contraseña |
|-----|-------|-----------|
| Administrador | admin@vetclinic.cl | admin123 |
| Recepcionista | recepcion@vetclinic.cl | recepcion123 |
| Veterinario | veterinario@vetclinic.cl | vet123 |
| Veterinario | ana.lopez@vetclinic.cl | vet123 |
| Veterinario | pedro.silva@vetclinic.cl | vet123 |

## 📁 Estructura del Proyecto

```
sistema_veterinaria/
├── autenticacion/          # App de autenticación
│   ├── forms.py           # Formulario de login
│   ├── models.py          # Modelo LoginAttempt
│   ├── views.py           # Vistas de login/logout
│   └── templates/
├── clientes/              # App de clientes
│   ├── forms.py           # Formularios de cliente
│   ├── models.py          # Modelo Cliente
│   ├── views.py           # CRUD de clientes
│   └── templates/
├── mascotas/              # App de mascotas
│   ├── forms.py           # Formularios de mascota
│   ├── models.py          # Modelo Mascota
│   ├── views.py           # CRUD de mascotas
│   └── templates/
├── usuarios/              # App de gestión de usuarios
│   ├── forms.py           # Formularios de usuario
│   ├── views.py           # CRUD de usuarios
│   └── templates/
├── core/                  # Funcionalidades compartidas
│   ├── utils.py           # Validadores y formateadores
│   └── management/
│       └── commands/
│           └── seed.py    # Comando para datos de prueba
├── static/                # Archivos estáticos
│   ├── css/
│   │   ├── main.css
│   │   ├── sidebar.css
│   │   └── forms.css
│   └── js/
│       └── main.js
├── templates/             # Templates globales
│   ├── base.html
│   └── base_with_sidebar.html
├── sistema_veterinaria/   # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env                   # Variables de entorno (no incluido en Git)
├── .env.example           # Ejemplo de variables de entorno
├── .gitignore
├── requirements.txt
├── manage.py
└── README.md
```

## 🔧 Funcionalidades por Rol

### Administrador
- ✅ Acceso completo a todas las funcionalidades
- ✅ Gestión de usuarios (crear, editar, activar/desactivar)
- ✅ Soft delete de clientes y mascotas
- ✅ Restablecimiento de contraseñas

### Recepcionista / Veterinario
- ✅ Gestión de clientes (crear, editar, ver)
- ✅ Gestión de mascotas (crear, editar, ver)
- ✅ Búsqueda de información
- ❌ No puede eliminar registros
- ❌ No puede acceder a gestión de usuarios

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5.3, Bootstrap Icons
- **Base de Datos**: SQLite (desarrollo)
- **Validaciones**: python-decouple para variables de entorno
- **Emails**: Django Email (SMTP)

## 📝 Validaciones Implementadas

### RUT Chileno
- Validación con algoritmo Módulo 11
- Formato automático: 12.345.678-9
- Verificación de dígito verificador

### Teléfono Chileno
- Formato automático: +56 9 8765 4321
- Validación de longitud y estructura

### Sistema de Soft Delete
- Los registros eliminados se marcan como `is_deleted=True`
- No se muestran en vistas normales
- Solo accesible para administradores

## 🎨 Paleta de Colores

```css
--color-primary: #2563EB        /* Azul principal */
--color-primary-light: #DBEAFE  /* Azul claro */
--color-success: #10B981        /* Verde */
--color-success-light: #D1FAE5  /* Verde claro */
--color-danger: #EF4444         /* Rojo */
--color-purple-light: #E9D5FF   /* Morado claro */
--color-gray-light: #F3F4F6     /* Gris claro */
--color-gray-text: #6B7280      /* Gris texto */
```

## 🔐 Seguridad

- ✅ Protección CSRF en todos los formularios
- ✅ Validación de permisos en todas las vistas
- ✅ Passwords hasheados con PBKDF2
- ✅ Sesiones seguras
- ✅ Sistema de bloqueo por intentos fallidos
- ✅ Variables sensibles en archivo .env

## 📧 Configuración de Emails

Para habilitar el envío de emails (credenciales de usuarios), configurar en `.env`:

### Gmail
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password  # Contraseña de aplicación, no tu contraseña normal
```

**Nota**: Para Gmail, debes generar una "Contraseña de aplicación" desde la configuración de seguridad de tu cuenta.

## 🧪 Comandos Útiles

### Crear superusuario
```bash
python manage.py createsuperuser
```

### Acceder al panel de administración
`http://localhost:8000/admin`

### Limpiar base de datos y recargar datos
```bash
python manage.py flush
python manage.py migrate
python manage.py seed
```

### Crear nueva migración
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📱 Navegación del Sistema

1. **Login** (`/`)
   - Iniciar sesión con credenciales
   - Recordar sesión
   - Autocompletado con usuarios de prueba

2. **Clientes y Mascotas** (`/clientes/`)
   - Vista unificada con switch de pestañas
   - Búsqueda en tiempo real
   - Cards informativos

3. **Gestión de Usuarios** (`/usuarios/`) - Solo Administradores
   - Tabla de usuarios
   - Crear/Editar usuarios
   - Activar/Desactivar
   - Restablecer contraseñas

## 🐛 Solución de Problemas

### Error: "No module named 'decouple'"
```bash
pip install python-decouple
```

### Error: "STATICFILES_DIRS"
Crear el directorio `static/` en la raíz del proyecto.

### Error de migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Los emails no se envían
- Verificar configuración en `.env`
- Para Gmail, usar contraseña de aplicación
- Revisar logs del servidor

## 🚧 Próximas Mejoras

- [ ] Dashboard con estadísticas
- [ ] Sistema de agenda y citas
- [ ] Gestión de consultas médicas
- [ ] Historial clínico de mascotas
- [ ] Reportes en PDF
- [ ] Recordatorios de vacunas
- [ ] Sistema de facturación

## 👨‍💻 Autor

Desarrollado para INACAP - Ingeniería de Software
Evaluación Sumativa IV

## 📄 Licencia

Este proyecto es de uso educativo.

---

**¿Necesitas ayuda?** Revisa la documentación de Django: https://docs.djangoproject.com/
