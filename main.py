import google.generativeai as genai
import google.generativeai as genai
import keyboard
from config import API_KEYS
from logic import procesar_input
from memory import guardar_interaccion, buscar_respuesta_similar
from  voice import escuchar, hablar

# =========================
# 🧠 CONFIGURACIÓN MODELO
# =========================
SYSTEM_INSTRUCTION = (
                        "Eres un asistente hospitalario profesional, claro y amable. "  
                        "Tus respuestas son cortas y precizas, tratas de no hablar mucho, ten pasienciaocn " 
                        "las palabras groseras y cuando hables con personas mayores, si no entides algo por que " 
                        "lo dijo muy bajito solo pide amable mente que lo repita peor "
                        "trata de no pedir esto siempre ya que el timepo es valioso," 
                        "si alguien dice emergencia notifica al urgencias, y indicas que se notifico"
                        "Informacion: Emergecia esta en el piso 1, en el ala este, informacion esta en entrada principal,"
                        " en un quiosco azul, la zona de UCI esta en el piso 1, ala oeste"
                        "luego de dar informacion indica si e;l ususario quiere terminar,4"
                        " asi otro puede comunicarse en una convesacion distinta" 
                        "habitacion de la 205 a la 305 piso 5" 
                        "habitacion de la 100 a la 205 piso 4" 
                        "CardiologiaÑ piso 3" 
                        "analisis piso 2" 
                        "emergecia piso 1" )

# ========== LISTADO DE MODELOS (con fallback) ==========
MODELOS_PRIORIDAD = ["gemini-2.5-flash", "gemma-3-1b-it", "gemma-3-4b-it", "gemma-3-12b-it"]


def crear_modelo(nombre_modelo):
    return genai.GenerativeModel(
        model_name=nombre_modelo,
        system_instruction=SYSTEM_INSTRUCTION
    )


# =========================
# 🤖 RESPUESTA IA (REAL)
# =========================
def responder_ia(texto):
    for api_key in API_KEYS:
        try:
            genai.configure(api_key=api_key)

            for modelo_nombre in MODELOS_PRIORIDAD:
                try:
                    modelo = crear_modelo(modelo_nombre)

                    response = modelo.generate_content(texto)

                    if response and hasattr(response, "text") and response.text:
                        return {
                            "respuesta": response.text.strip(),
                            "api": api_key,
                            "modelo": modelo_nombre
                        }

                except Exception as e:
                    error = str(e)

                    if "429" in error:
                        break

                    if "not found" in error.lower():
                        continue

                    continue

        except:
            continue

    return {
        "respuesta": "Todos los servicios están ocupados. Intenta más tarde.",
        "api": None,
        "modelo": None
    }


# =========================
# 💬 CHAT PRINCIPAL
# =========================
import keyboard

def obtener_input():
    print("\n[ENTER = escribir | V = voz | salir = terminar]")

    tecla = keyboard.read_key()

    if tecla == 'v':
        try:
            entrada = escuchar()
            if not entrada:
                print("⚠️ No se detectó voz")
                return None
            print(f"Tú (voz): {entrada}")
            return entrada
        except Exception as e:
            print("⚠️ Error en reconocimiento de voz:", e)
            return None
    else:
        entrada = input("Tú: ").strip()
        return entrada if entrada else None


def procesar_respuesta(user_input):
    # 🔍 1. Base de datos
    respuesta, tipo = procesar_input(user_input)
    if not respuesta:
        # 🔍 2. Memoria
        respuesta = buscar_respuesta_similar(user_input)
        tipo = "memoria" if respuesta else None
        

    if not respuesta:
        # 🤖 3. IA
        resultado = responder_ia(user_input)

        print("\n==============================")
        print(f"API usada: {resultado['api']}")
        print(f"Modelo: {resultado['modelo']}")
        print("==============================")

        respuesta = resultado["respuesta"]
        tipo = "ia"

        if not respuesta or "Error" in respuesta:
            return None, None

    return respuesta, tipo


def ejecutar_respuesta(user_input, respuesta, tipo):
    print(f"{tipo.upper() if tipo else 'RESPUESTA'}:", respuesta)
    hablar(respuesta)

    if tipo:
        guardar_interaccion(user_input, respuesta, tipo)


def chat():
    print("🤖 Asistente iniciado (presiona 'S' para salir)\n")

    modo_voz = False

    while True:
        try:
            # 🔴 Detectar salida en cualquier momento
            if keyboard.is_pressed('s'):
                print("\n👋 Cerrando asistente...")
                break

            if not modo_voz:
                print("\n[ENTER = escribir | V = voz continua | S = salir]")
                tecla = keyboard.read_key()

                if tecla == 'v':
                    modo_voz = True
                    print("🎤 Modo voz ACTIVADO")
                    continue
                elif tecla == 's':
                    print("👋 Cerrando asistente...")
                    break
                else:
                    user_input = input("Tú: ").strip()
            else:
                # 🎤 modo voz continuo
                user_input = escuchar()

                if not user_input:
                    continue

                print(f"Tú (voz): {user_input}")

            # 🔴 comando por texto también (opcional)
            if user_input.lower() == "salir":
                print("👋 Cerrando asistente...")
                break

            if user_input.lower() == "modo texto":
                modo_voz = False
                print("⌨️ Modo texto ACTIVADO")
                continue

            # 🔍 procesamiento
            respuesta, tipo = procesar_respuesta(user_input)

            if respuesta:
                ejecutar_respuesta(user_input, respuesta, tipo)
            else:
                print("⚠️ No se pudo generar respuesta")

        except KeyboardInterrupt:
            print("\n👋 Interrumpido")
            break
        except Exception as e:
            print("\n[ERROR]:", str(e))

if __name__ == "__main__":
    chat()