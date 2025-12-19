"""
Comando para poblar la base de datos con datos de prueba
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from clientes.models import Cliente
from mascotas.models import Mascota
from datetime import date
import os


class Command(BaseCommand):
    help = 'Poblar la base de datos con datos de prueba'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina la base de datos y todas las migraciones, luego la recrea desde cero',
        )

    def handle(self, *args, **kwargs):
        reset = kwargs.get('reset', False)
        
        if reset:
            self.stdout.write(self.style.WARNING('\n⚠️  ADVERTENCIA: Esto eliminará TODOS los datos y migraciones'))
            confirm = input('¿Estás seguro? Escribe "SI" para confirmar: ')
            
            if confirm != 'SI':
                self.stdout.write(self.style.ERROR('Operación cancelada'))
                return
            
            self.reset_database()
        
        self.seed_data()

    def reset_database(self):
        """Elimina la base de datos y las migraciones, y las recrea"""
        from django.conf import settings
        from django.db import connections
        import shutil
        import time
        
        self.stdout.write(self.style.WARNING('\n🗑️  Eliminando base de datos...'))
        
        # Cerrar todas las conexiones activas
        for conn in connections.all():
            conn.close()
        
        # Eliminar archivo de base de datos SQLite
        db_path = settings.DATABASES['default']['NAME']
        if os.path.exists(db_path):
            # Intentar varias veces con pequeñas pausas
            max_attempts = 5
            for attempt in range(max_attempts):
                try:
                    os.remove(db_path)
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Base de datos eliminada: {db_path}'))
                    break
                except PermissionError:
                    if attempt < max_attempts - 1:
                        self.stdout.write(self.style.WARNING(f'  ⏳ Esperando... (intento {attempt + 1}/{max_attempts})'))
                        time.sleep(1)
                    else:
                        self.stdout.write(self.style.ERROR(
                            '\n❌ Error: No se pudo eliminar la base de datos.\n'
                            '   Cierra todas las conexiones (VS Code, navegador, etc.) y ejecuta:\n'
                            '   py manage.py seed --reset\n'
                        ))
                        return
        
        # Eliminar carpetas de migraciones
        self.stdout.write(self.style.WARNING('\n🗑️  Eliminando archivos de migraciones...'))
        apps = ['autenticacion', 'clientes', 'mascotas', 'core']
        
        for app in apps:
            migrations_path = os.path.join(app, 'migrations')
            if os.path.exists(migrations_path):
                # Eliminar todos los archivos excepto __init__.py
                for file in os.listdir(migrations_path):
                    if file != '__init__.py' and file != '__pycache__':
                        file_path = os.path.join(migrations_path, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                self.stdout.write(self.style.SUCCESS(f'  ✓ Migraciones eliminadas: {app}'))
        
        # Ejecutar makemigrations y migrate
        self.stdout.write(self.style.WARNING('\n📝 Creando nuevas migraciones...'))
        from django.core.management import call_command
        call_command('makemigrations')
        
        self.stdout.write(self.style.WARNING('\n🔄 Aplicando migraciones...'))
        call_command('migrate')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Base de datos recreada exitosamente\n'))

    def seed_data(self):
        """Pobla la base de datos con datos de prueba"""
        self.stdout.write(self.style.SUCCESS('Iniciando seed de datos...'))
        
        # Crear grupos
        self.stdout.write('Creando grupos...')
        admin_group, _ = Group.objects.get_or_create(name='Administrador')
        recepcionista_group, _ = Group.objects.get_or_create(name='Recepcionista')
        veterinario_group, _ = Group.objects.get_or_create(name='Veterinario')
        
        # Crear usuarios de prueba
        self.stdout.write('Creando usuarios...')
        
        # Administrador
        if not User.objects.filter(email='admin@vetclinic.cl').exists():
            admin = User.objects.create_user(
                username='admin',
                email='admin@vetclinic.cl',
                password='admin123',
                first_name='María',
                last_name='Admin',
                is_staff=True,
                is_superuser=True
            )
            admin.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Usuario administrador creado: admin@vetclinic.cl / admin123'))
        
        # Recepcionista
        if not User.objects.filter(email='recepcion@vetclinic.cl').exists():
            recepcionista = User.objects.create_user(
                username='recepcion',
                email='recepcion@vetclinic.cl',
                password='recepcion123',
                first_name='Ana',
                last_name='García',
                is_staff=True
            )
            recepcionista.groups.add(recepcionista_group)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Usuario recepcionista creado: recepcion@vetclinic.cl / recepcion123'))
        
        # Veterinarios
        veterinarios_data = [
            {'username': 'veterinario', 'email': 'veterinario@vetclinic.cl', 'password': 'vet123', 
             'first_name': 'Dr. Carlos', 'last_name': 'Méndez'},
            {'username': 'analopez', 'email': 'ana.lopez@vetclinic.cl', 'password': 'vet123',
             'first_name': 'Dra. Ana', 'last_name': 'López'},
            {'username': 'pedrosilva', 'email': 'pedro.silva@vetclinic.cl', 'password': 'vet123',
             'first_name': 'Dr. Pedro', 'last_name': 'Silva'},
        ]
        
        for vet_data in veterinarios_data:
            if not User.objects.filter(email=vet_data['email']).exists():
                vet = User.objects.create_user(
                    username=vet_data['username'],
                    email=vet_data['email'],
                    password=vet_data['password'],
                    first_name=vet_data['first_name'],
                    last_name=vet_data['last_name'],
                    is_staff=True
                )
                vet.groups.add(veterinario_group)
                self.stdout.write(self.style.SUCCESS(f'  ✓ Usuario veterinario creado: {vet_data["email"]} / {vet_data["password"]}'))
        
        # Crear una recepcionista inactiva
        if not User.objects.filter(email='pedro@vetclinic.cl').exists():
            pedro = User.objects.create_user(
                username='pedrorecep',
                email='pedro@vetclinic.cl',
                password='pedro123',
                first_name='Pedro',
                last_name='Recepción',
                is_staff=True,
                is_active=False
            )
            pedro.groups.add(recepcionista_group)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Usuario inactivo creado: pedro@vetclinic.cl (Inactivo)'))
        
        # Crear clientes de prueba
        self.stdout.write('Creando clientes...')
        
        clientes_data = [
            {
                'nombre': 'Juan Pérez',
                'rut': '21.270.857-7',
                'telefono': '+56 9 8765 4321',
                'email': 'juan@email.cl'
            },
            {
                'nombre': 'María González',
                'rut': '8.808.668-6',
                'telefono': '+56 9 1234 5678',
                'email': 'maria@email.cl'
            },
            {
                'nombre': 'Carlos Rodríguez',
                'rut': '17.534.145-5',
                'telefono': '+56 9 5555 6666',
                'email': 'carlos@email.cl'
            },
            {
                'nombre': 'Sofía Martínez',
                'rut': '12.333.673-9',
                'telefono': '+56 9 7777 8888',
                'email': 'sofia@email.cl'
            },
        ]
        
        clientes_creados = {}
        for cliente_data in clientes_data:
            cliente, created = Cliente.objects.get_or_create(
                rut=cliente_data['rut'],
                defaults=cliente_data
            )
            clientes_creados[cliente_data['nombre']] = cliente
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Cliente creado: {cliente_data["nombre"]}'))
        
        # Crear mascotas de prueba
        self.stdout.write('Creando mascotas...')
        
        mascotas_data = [
            {
                'dueno': clientes_creados['Juan Pérez'],
                'nombre': 'Max',
                'especie': 'Perro',
                'raza': 'Labrador',
                'sexo': 'Macho',
                'edad': 4,
                'fecha_nacimiento': date(2021, 12, 13),
                'alergias': None
            },
            {
                'dueno': clientes_creados['María González'],
                'nombre': 'Luna',
                'especie': 'Gato',
                'raza': 'Siamés',
                'sexo': 'Hembra',
                'edad': 3,
                'fecha_nacimiento': date(2022, 12, 13),
                'alergias': None
            },
            {
                'dueno': clientes_creados['María González'],
                'nombre': 'Rocky',
                'especie': 'Perro',
                'raza': 'Pastor Alemán',
                'sexo': 'Macho',
                'edad': 6,
                'fecha_nacimiento': date(2019, 12, 13),
                'alergias': 'Alergia a algunos tipos de pasto'
            },
            {
                'dueno': clientes_creados['Carlos Rodríguez'],
                'nombre': 'Michi',
                'especie': 'Gato',
                'raza': 'Persa',
                'sexo': 'Hembra',
                'edad': 4,
                'fecha_nacimiento': date(2020, 12, 13),
                'alergias': None
            },
            {
                'dueno': clientes_creados['Sofía Martínez'],
                'nombre': 'Pipo',
                'especie': 'Ave',
                'raza': 'Loro',
                'sexo': 'Macho',
                'edad': 8,
                'fecha_nacimiento': date(2017, 12, 13),
                'alergias': None
            },
            {
                'dueno': clientes_creados['Sofía Martínez'],
                'nombre': 'Toby',
                'especie': 'Roedor',
                'raza': 'Hámster Sirio',
                'sexo': 'Macho',
                'edad': 2,
                'fecha_nacimiento': date(2023, 12, 13),
                'alergias': None
            },
        ]
        
        for mascota_data in mascotas_data:
            mascota, created = Mascota.objects.get_or_create(
                nombre=mascota_data['nombre'],
                dueno=mascota_data['dueno'],
                defaults=mascota_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Mascota creada: {mascota_data["nombre"]} ({mascota_data["especie"]}) - {mascota_data["dueno"].nombre}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Seed completado exitosamente'))
        self.stdout.write(self.style.SUCCESS('\nUsuarios creados:'))
        self.stdout.write('  - Administrador: admin@vetclinic.cl / admin123')
        self.stdout.write('  - Recepcionista: recepcion@vetclinic.cl / recepcion123')
        self.stdout.write('  - Veterinario: veterinario@vetclinic.cl / vet123')
        self.stdout.write('  - Veterinario: ana.lopez@vetclinic.cl / vet123')
        self.stdout.write('  - Veterinario: pedro.silva@vetclinic.cl / vet123')
        self.stdout.write('  - Inactivo: pedro@vetclinic.cl (Inactivo)\n')
