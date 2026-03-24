pacientes = {
    "00112345678": {
        "nombre": "Juan Pérez",
        "cita": "Cardiología - 10:00 AM",
        "estado": "En espera"
    },
    "40298765432": {
        "nombre": "Ana Gómez",
        "cita": "Dermatología - 2:30 PM",
        "estado": "Confirmada"
    }
}

def buscar_paciente(cedula):
    return pacientes.get(cedula, None)