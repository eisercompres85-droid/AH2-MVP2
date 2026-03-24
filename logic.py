import re
from database import buscar_paciente

def extraer_cedula(texto):
    match = re.search(r'\d{11}', texto)
    return match.group(0) if match else None


def procesar_input(texto):
    cedula = extraer_cedula(texto)

    if cedula:
        paciente = buscar_paciente(cedula)
        if paciente:
            return f"""Paciente encontrado:
Nombre: {paciente['nombre']}
Cita: {paciente['cita']}
Estado: {paciente['estado']}""", "db"
        else:
            return "No se encontró ningún paciente con esa cédula.", "db"

    return None, None