import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("La variable de entorno OPENAI_API_KEY no está definida.")


client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-4o",  # Puedes usar también gpt-4 o gpt-3.5-turbo
    messages=[
        {"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}
    ],
    temperature=0.7,
)


print(response.choices[0].message.content)
