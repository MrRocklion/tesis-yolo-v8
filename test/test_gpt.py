import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("La variable de entorno OPENAI_API_KEY no está definida.")

# Inicializar cliente
client = OpenAI(api_key=api_key)

# Enviar mensaje usando el modelo GPT-4o
response = client.chat.completions.create(
    model="gpt-4o",  # Puedes usar también gpt-4 o gpt-3.5-turbo
    messages=[
        {"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}
    ],
    temperature=0.7,
)

# Mostrar la respuesta
print(response.choices[0].message.content)
