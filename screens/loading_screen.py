from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QObject, QThread, Signal
import requests
from widgets.loading import LoadingWidget
import os
from openai import OpenAI
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import pathlib
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
service_account_info = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
}
if not api_key:
    raise ValueError("La variable de entorno OPENAI_API_KEY no está definida.")
client = OpenAI(api_key=api_key)
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

db = firestore.client()

class DataProcessor(QObject):
    finished = Signal(dict, str)  # resultado, clase detectada
    error = Signal(str)

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def run(self):
        try:
            url = "https://predict.ultralytics.com"
            headers = {"x-api-key": "0a9bc0db09f57ab77a254e400877b03f91ac946e5d"}
            data = {
                "model": "https://hub.ultralytics.com/models/5NOJhLhigIjjuOABqyUQ",
                "imgsz": 640,
                "conf": 0.25,
                "iou": 0.45
            }
            with open("target.jpg", "rb") as f:
                response = requests.post(url, headers=headers, data=data, files={"file": f})
            response.raise_for_status()
            result = response.json()

            name_class = result['images'][0]['results'][0]['name']
            data_promt = {
                "age": self.controller.get_age(),
                "mood": self.controller.get_emotion(),
                "gender": self.controller.get_gender(),
                "class": name_class,
                "name": self.controller.get_name(),
                "prediction":"",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "created_at": firestore.SERVER_TIMESTAMP,
                "file_name":""
            }
            # prompt = f'''
            #     Generate an explanatory paragraph in spanish adapted for a child diagnosed with Autism Spectrum Disorder (ASD), about the word "{data_promt["class"]}". 
            #     The explanation should:
            #     - Use simple, clear, and concrete language.
            #     - Describe what the word means and how it is used in daily life.
            #     - Include examples that relate to the childs world and help improve their semantic understanding.
            #     Take into account:
            #     - The child's current mood: {data_promt["mood"]}
            #     - The child's age: {data_promt["age"]} years old
            #     - The child's gender: {data_promt["gender"]}
            #     Make the explanation friendly, supportive, and emotionally sensitive based on the child's mood.
            #     '''
            prompt = f'''
                    Generate an explanatory paragraph in spanish adapted for a child named {data_promt['name']} diagnosed with Autism Spectrum Disorder (ASD), about the word "{data_promt["class"]}".
                    The child is {data_promt["age"]} years old, {data_promt["gender"]}, and currently feeling {data_promt["mood"]}.
                    Use simple, clear, and concrete language. Help the child understand what the word means and how it relates to their daily life. Give examples that make sense for a child of that age and emotional state.
                    The explanation should be friendly and supportive. Please give a direct explanation — do not include placeholders or fields in brackets like [name]
                    **Limit the explanatory paragraph to no more than 80 words.**
                    '''

            response = client.chat.completions.create(
                model="gpt-4o",  
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            chat_gtp_response = response.choices[0].message.content
            data_promt["prediction"] = chat_gtp_response
            db.collection("inferences").add(data_promt)
            carpeta_audio = pathlib.Path("audio")
            carpeta_audio.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ruta_salida = carpeta_audio / f"salida_{timestamp}.mp3"
            with client.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice="alloy",
                input=chat_gtp_response,
            ) as respuesta:
                respuesta.stream_to_file(ruta_salida)
            data_promt["file_name"] = f"salida_{timestamp}.mp3"
            self.finished.emit(data_promt, chat_gtp_response)

        except Exception as e:
            self.error.emit(str(e))


class LoadingScreen(QWidget):
    def __init__(self, stacked_widget, controller):
        super().__init__()
        self.controller = controller
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        loading = LoadingWidget()
        layout.addWidget(loading)
        self.setLayout(layout)

    def process_data(self):
        self.thread = QThread()
        self.worker = DataProcessor(self.controller)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_processing_finished)
        self.worker.error.connect(self.on_processing_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_processing_finished(self, data_promt, chat_gtp_response):
        print(data_promt)
        self.controller.set_gpt_prediction(chat_gtp_response)
        self.stacked_widget.setCurrentIndex(7)


    def on_processing_error(self, error_message):
        print(f"Error al procesar los datos: {error_message}")
        self.stacked_widget.setCurrentIndex(1)
