from openai import OpenAI
import pathlib
from dotenv import load_dotenv
import os
from datetime import datetime
# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
texto = "Hola David, este audio fue generado con la API de OpenAI usando Python."
carpeta_audio = pathlib.Path("audio")
carpeta_audio.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
ruta_salida = carpeta_audio / f"salida_{timestamp}.mp3"
with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="alloy",
    input=texto,
) as respuesta:
    respuesta.stream_to_file(ruta_salida)

print(f"✅ Audio generado y guardado en {ruta_salida}")
