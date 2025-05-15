from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QObject, QThread, Signal
import requests
from widgets.loading import LoadingWidget
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("La variable de entorno OPENAI_API_KEY no está definida.")
client = OpenAI(api_key=api_key)

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
            }
            promt = f'''
                Generate an explanatory paragraph in spanish adapted for a child diagnosed with Autism Spectrum Disorder (ASD), about the word "{data_promt["class"]}". 

                The explanation should:
                - Use simple, clear, and concrete language.
                - Describe what the word means and how it is used in daily life.
                - Include examples that relate to the childs world and help improve their semantic understanding.

                Take into account:
                - The child's current mood: {data_promt["mood"]}
                - The child's age: {data_promt["age"]} years old
                - The child's gender: {data_promt["gender"]}

                Make the explanation friendly, supportive, and emotionally sensitive based on the child's mood.

                '''
            response = client.chat.completions.create(
                model="gpt-4o",  # Puedes usar también gpt-4 o gpt-3.5-turbo
                messages=[
                    {"role": "user", "content": promt}
                ],
                temperature=0.7,
            )
            chat_gtp_response = response.choices[0].message.content
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
