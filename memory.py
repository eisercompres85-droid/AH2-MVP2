import json
from datetime import datetime

ARCHIVO = "historial.json"

def guardar_interaccion(user_input, respuesta, tipo):
    data = {
        "input": user_input,
        "output": respuesta,
        "tipo": tipo,
        "timestamp": str(datetime.now())
    }

    try:
        with open(ARCHIVO, "r") as f:
            historial = json.load(f)
    except:
        historial = []

    historial.append(data)

    with open(ARCHIVO, "w") as f:
        json.dump(historial, f, indent=4)


def cargar_historial():
    try:
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    except:
        return []   
    

def buscar_respuesta_similar(pregunta):
    historial = cargar_historial()

    pregunta = pregunta.lower()

    for item in reversed(historial):  # busca lo más reciente primero
        if pregunta in item["input"].lower():
            return item["output"]

    return None