from PySide6.QtWidgets import (
    QWidget,QVBoxLayout,QLabel
)
import requests
from widgets.loading import LoadingWidget
class LoadingScreen(QWidget):
    def __init__(self, stacked_widget,controller):
        super().__init__()
        self.controller = controller
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()
        loading = LoadingWidget()
        layout.addWidget(loading)
        self.setLayout(layout)
    

    def process_data(self):
        # Simulando un proceso de carga
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
        self.controller.set_class_object(name_class)
        self.stacked_widget.setCurrentIndex(7)
        print(f"✅ Objeto '{name_class}' identificado correctamente durante {self.detection_duration} segundos.")