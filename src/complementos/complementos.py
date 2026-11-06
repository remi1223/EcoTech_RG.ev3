import os
import re

def limpiar_pantalla():
    os.system("cls")

def validar_texto_longitud(texto: str, max_longitud: int = 50, campo: str = "Texto") -> str:

    texto_limpio = texto.strip()
    if not texto_limpio:
        raise ValueError(f"El campo '{campo}' no puede estar vacío.")
    if len(texto_limpio) > max_longitud:
        raise ValueError(f"El campo '{campo}' no puede exceder los {max_longitud} caracteres (longitud actual: {len(texto_limpio)}).")
    return texto_limpio


def validar_nombre(nombre: str, max_longitud: int = 50) -> str:
    nombre_limpio = validar_texto_longitud(nombre, max_longitud=max_longitud, campo="Nombre")
    patron = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
    if not re.match(patron, nombre_limpio):
        raise ValueError("El nombre solo debe contener letras y espacios.")
    return nombre_limpio.title()


def validar_correo(correo: str, max_longitud: int = 100) -> str:
    correo_limpio = validar_texto_longitud(correo, max_longitud=max_longitud, campo="Correo electrónico")
    patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(patron, correo_limpio):
        raise ValueError("El formato del correo electrónico es inválido (ejemplo: usuario@dominio.com).")
    return correo_limpio.lower()


def validar_telefono(telefono: str) -> str:
    telefono_limpio = telefono.strip()
    patron = r"^\+?[0-9]{7,15}$"
    if not re.match(patron, telefono_limpio):
        raise ValueError("El número de teléfono debe contener entre 7 y 15 dígitos (opcionalmente iniciando con '+').")
    return telefono_limpio

def validar_entero_positivo(valor: str, campo: str = "Número") -> int:
    try:
        num = int(valor.strip())
        if num < 0:
            raise ValueError(f"El campo '{campo}' no puede ser negativo.")
        return num
    except ValueError:
        raise ValueError(f"El campo '{campo}' debe ser un número entero válido.")


def validar_flotante_positivo(valor: str, campo: str = "Monto") -> float:
    try:
        num = float(valor.strip())
        if num < 0:
            raise ValueError(f"El campo '{campo}' no puede ser negativo.")
        return num
    except ValueError:
        raise ValueError(f"El campo '{campo}' debe ser un número válido.")


def validar_salario(salario_str: str, min_salario: float = 0.0, max_salario: float = 5000000.0) -> float:
    salario = validar_flotante_positivo(salario_str, campo="Salario")
    if salario < min_salario:
        raise ValueError(f"El salario no puede ser menor a ${min_salario:,.2f}.")
    if salario > max_salario:
        raise ValueError(f"El salario ingresado excede el límite permitido (${max_salario:,.2f}).")
    return salario

def validar_fecha_YYYY_MM_DD(fecha_str: str) -> str:
    from datetime import datetime
    fecha_limpia = fecha_str.strip()
    try:
        fecha_obj = datetime.strptime(fecha_limpia, "%d-%m-%Y")
        return fecha_obj.strftime("%d-%m-%Y")
    except ValueError:
        raise ValueError("La fecha debe tener el formato DD-MM-YYYY (ejemplo: 30-05-2026).")