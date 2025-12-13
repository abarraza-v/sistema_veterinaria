"""
Utilidades para validación y formato de datos chilenos
"""
import re


def limpiar_rut(rut):
    """
    Elimina puntos y guiones del RUT
    Args:
        rut: String con el RUT a limpiar
    Returns:
        String con el RUT sin formato
    """
    return re.sub(r'[.-]', '', str(rut))


def validar_rut(rut):
    """
    Valida un RUT chileno usando el algoritmo Módulo 11
    Args:
        rut: String con el RUT a validar (puede incluir puntos y guión)
    Returns:
        Boolean indicando si el RUT es válido
    """
    rut_limpio = limpiar_rut(rut)
    
    # Verificar que tenga al menos 2 caracteres (número + dígito verificador)
    if len(rut_limpio) < 2:
        return False
    
    # Separar número y dígito verificador
    numero = rut_limpio[:-1]
    dv = rut_limpio[-1].upper()
    
    # Verificar que el número sea numérico
    if not numero.isdigit():
        return False
    
    # Calcular dígito verificador esperado
    suma = 0
    multiplicador = 2
    
    for digito in reversed(numero):
        suma += int(digito) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador < 7 else 2
    
    resto = suma % 11
    dv_esperado = '0' if resto == 11 else 'K' if resto == 10 else str(11 - resto)
    
    return dv == dv_esperado


def formatear_rut(rut):
    """
    Formatea un RUT al formato chileno: 12.345.678-9
    Args:
        rut: String con el RUT a formatear
    Returns:
        String con el RUT formateado o el original si es inválido
    """
    rut_limpio = limpiar_rut(rut)
    
    if not validar_rut(rut_limpio):
        return rut
    
    # Separar número y dígito verificador
    numero = rut_limpio[:-1]
    dv = rut_limpio[-1].upper()
    
    # Formatear con puntos de miles
    numero_formateado = f"{int(numero):,}".replace(',', '.')
    
    return f"{numero_formateado}-{dv}"


def limpiar_telefono(telefono):
    """
    Elimina todos los caracteres no numéricos del teléfono
    Args:
        telefono: String con el teléfono a limpiar
    Returns:
        String con solo los números
    """
    return re.sub(r'\D', '', str(telefono))


def validar_telefono_chileno(telefono):
    """
    Valida que un teléfono chileno tenga el formato correcto
    Args:
        telefono: String con el teléfono a validar
    Returns:
        Boolean indicando si el teléfono es válido
    """
    telefono_limpio = limpiar_telefono(telefono)
    
    # Debe tener entre 8 y 11 dígitos (código país + número)
    # 56 + 9 + 8 dígitos = 11 dígitos para celulares
    # 8 dígitos para teléfonos fijos sin código país
    if len(telefono_limpio) < 8 or len(telefono_limpio) > 11:
        return False
    
    return True


def formatear_telefono_chileno(telefono):
    """
    Formatea un teléfono al formato chileno: +56 9 8765 4321
    Args:
        telefono: String con el teléfono a formatear
    Returns:
        String con el teléfono formateado
    """
    telefono_limpio = limpiar_telefono(telefono)
    
    if not validar_telefono_chileno(telefono_limpio):
        return telefono
    
    # Si no tiene código de país, agregarlo
    if not telefono_limpio.startswith('56'):
        telefono_limpio = '56' + telefono_limpio
    
    # Formato: +56 9 8765 4321
    if len(telefono_limpio) == 11 and telefono_limpio.startswith('56'):
        return f"+{telefono_limpio[:2]} {telefono_limpio[2]} {telefono_limpio[3:7]} {telefono_limpio[7:]}"
    elif len(telefono_limpio) == 10 and telefono_limpio.startswith('569'):
        return f"+56 {telefono_limpio[2]} {telefono_limpio[3:7]} {telefono_limpio[7:]}"
    else:
        # Para fijos u otros formatos
        return f"+56 {telefono_limpio[2:]}"
