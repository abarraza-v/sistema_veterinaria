// JavaScript principal del proyecto

// Confirmación de eliminación
function confirmDelete(message) {
    return confirm(message || '¿Estás seguro de que deseas eliminar este elemento?');
}

// Mostrar/ocultar campo de especie_otro en formulario de mascotas
document.addEventListener('DOMContentLoaded', function() {
    const especieSelect = document.getElementById('id_especie');
    const especieOtroWrapper = document.getElementById('especie_otro_wrapper');
    
    if (especieSelect && especieOtroWrapper) {
        especieSelect.addEventListener('change', function() {
            if (this.value === 'Otro') {
                especieOtroWrapper.classList.add('show');
                document.getElementById('id_especie_otro').required = true;
            } else {
                especieOtroWrapper.classList.remove('show');
                document.getElementById('id_especie_otro').required = false;
            }
        });
        
        // Verificar al cargar la página
        if (especieSelect.value === 'Otro') {
            especieOtroWrapper.classList.add('show');
        }
    }
});

// Auto-dismiss alerts después de 5 segundos
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Formatear RUT mientras se escribe
function formatRUT(input) {
    let value = input.value.replace(/[^0-9kK]/g, '');
    
    if (value.length > 1) {
        let dv = value.slice(-1);
        let number = value.slice(0, -1);
        
        // Formatear con puntos
        number = number.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        
        input.value = number + '-' + dv;
    }
}

// Formatear teléfono chileno mientras se escribe
function formatPhone(input) {
    let value = input.value.replace(/\D/g, '');
    
    if (value.startsWith('56')) {
        // +56 9 8765 4321
        if (value.length >= 11) {
            input.value = '+' + value.slice(0, 2) + ' ' + value.slice(2, 3) + ' ' + 
                          value.slice(3, 7) + ' ' + value.slice(7, 11);
        }
    } else if (value.length >= 9) {
        // Agregar +56 automáticamente
        input.value = '+56 ' + value.slice(0, 1) + ' ' + value.slice(1, 5) + ' ' + value.slice(5, 9);
    }
}

// Toggle para sidebar en móvil
document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }
});
