# Guía de Inicio Rápido - Veterinaria "Patitas Felices"

## Instalación Express

### 1. Activar el entorno virtual
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Instalar dependencias (si aún no lo has hecho)
```bash
pip install -r requirements.txt
```

### 3. Aplicar migraciones
```bash
python manage.py migrate
```

### 4. Cargar datos de prueba
```bash
python manage.py seed
```

### 5. Iniciar el servidor
```bash
python manage.py runserver
```

### 6. Acceder al sistema
Abrir navegador en: **http://localhost:8000**

## Credenciales de Acceso

| Usuario | Email | Contraseña | Permisos |
|---------|-------|------------|----------|
| Admin | admin@vetclinic.cl | admin123 | Todos |
| Recepcionista | recepcion@vetclinic.cl | recepcion123 | Ver/Crear/Editar |
| Veterinario | veterinario@vetclinic.cl | vet123 | Ver/Crear/Editar |

## Navegación Rápida

### Login
- URL: `/` o `/login/`
- Click en usuarios de prueba para autocompletar

### Clientes y Mascotas
- URL: `/clientes/`
- Switch entre Clientes/Mascotas
- Búsqueda en tiempo real
- Crear/Editar con formularios validados

### Gestión de Usuarios (Solo Admin)
- URL: `/usuarios/`
- Crear usuarios con contraseña automática
- Activar/Desactivar usuarios
- Restablecer contraseñas

## Funcionalidades Destacadas

### ✅ Validaciones Automáticas
- **RUT chileno**: Formato 12.345.678-9 con validación Módulo 11
- **Teléfono**: Formato +56 9 8765 4321

### ✅ Seguridad
- Sistema de bloqueo: 5 intentos fallidos = 5 minutos de bloqueo
- Soft delete: Los registros eliminados no se borran permanentemente
- Protección por roles: Administrador puede eliminar, otros roles no

### ✅ Vista Unificada
- Clientes y Mascotas en una sola página
- Switch de pestañas intuitivo
- Cards informativos con relaciones

## 🛠️ Comandos Útiles

### Reiniciar la base de datos
```bash
python manage.py flush
python manage.py migrate
python manage.py seed
```

### Crear un superusuario adicional
```bash
python manage.py createsuperuser
```

### Acceder al panel de administración
```
http://localhost:8000/admin
```

## Datos de Ejemplo Incluidos

Después de ejecutar `python manage.py seed`:

- **6 usuarios** (1 Admin, 2 Recepcionistas, 3 Veterinarios)
- **4 clientes** con datos completos
- **6 mascotas** asociadas a los clientes
- **3 grupos** (Administrador, Recepcionista, Veterinario)

## 🔴 Solución Rápida de Problemas

### El servidor no inicia
```bash
# Verificar que el entorno virtual esté activado
# Debe aparecer (venv) al inicio de la línea de comando
```

### Error "No module named..."
```bash
pip install -r requirements.txt
```

### Los estilos no cargan
```bash
# Verificar que existe el directorio static/
# El servidor debe mostrar: [GET] /static/css/...
```

### Error de base de datos
```bash
python manage.py migrate
```

## Estructura de Archivos Importante

```
sistema_veterinaria/
├── db.sqlite3              # Base de datos (no subir a Git)
├── manage.py               # Comando principal de Django
├── requirements.txt        # Dependencias del proyecto
├── .env                    # Variables de entorno (no subir a Git)
├── README.md              # Documentación completa
└── QUICKSTART.md          # Esta guía
```

## Tips de Uso

1. **Siempre activar el entorno virtual** antes de trabajar
2. **Usar usuarios de prueba** para probar las funcionalidades
3. **El administrador** tiene acceso a todo, incluyendo eliminación
4. **Recepcionistas y Veterinarios** pueden ver, crear y editar, pero no eliminar
5. **Los RUT y teléfonos** se formatean automáticamente al salir del campo
 Revisa el README.md para más detalles

---

**¿Necesitas más ayuda?** Consulta el README.md completo o la documentación de Django.
