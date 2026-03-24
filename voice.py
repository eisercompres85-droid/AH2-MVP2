import queue
import json
import os
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import pyttsx3

# =========================
# 🔊 VOZ
# =========================
def hablar(texto):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1)

        engine.say(texto)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print("Error en voz:", e)


# =========================
# 🎤 CONFIG VOSK
# =========================
q = queue.Queue()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "vosk-model-small-es-0.42")

print("📂 Cargando modelo desde:", MODEL_PATH)

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)


def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))


# =========================
# 🎧 ESCUCHAR
# =========================
def escuchar():
    try:
        print("\n🎤 Escuchando...")

        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype='int16',
            channels=1,
            callback=callback
        ):
            while True:
                data = q.get()

                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    texto = result.get("text", "")

                    if texto:
                        print("🗣️ Dijiste:", texto)
                        return texto

    except Exception as e:
        print("⚠️ Error en micrófono:", str(e))
        return None