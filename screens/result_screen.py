from PySide6.QtWidgets import (QWidget, QVBoxLayout,QLabel,QHBoxLayout)
from PySide6.QtCore import Qt
from widgets.custom_btn import CustomButton
import os
import pathlib
import subprocess
class ResultScreen(QWidget):
    def __init__(self, stacked_widget,controller):
        super().__init__()
        self.controller = controller
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
        """)
        self.result_label.setWordWrap(True)
      
        #BOTONES
        self.btn_retry = CustomButton("Reintentar",base_color="#6200EE")
        self.btn_back = CustomButton("Volver al menu",base_color="#58d68d")
        self.btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_retry.clicked.connect(lambda: self.retry_event())


        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.btn_retry)
        horizontal_layout.setSpacing(20)
        horizontal_layout.addWidget(self.btn_back)
        layout.addWidget(self.result_label)
        layout.addSpacing(20)
        layout.addLayout(horizontal_layout)

        self.controller.gptPredictionChanged.connect(self.see_result)
        self.controller.fileNameChanged.connect(self._play_sound)

        self.setLayout(layout)
    def see_result(self, prediction):
        self.result_label.setText(prediction)
        
    def retry_event(self):
        self.stacked_widget.setCurrentIndex(5)
        self.controller.set_yolo(True)
    
    def reproducir_audio(self,file_name):
        ruta = pathlib.Path("audio") / file_name
        
        if not ruta.exists():
            print(f"El archivo {ruta} no existe.")
            return
        
        try:
            print(f"Reproduciendo: {ruta}")
            os.system(f"mpg123 {ruta}")
        except Exception as e:
            print(f"Error al reproducir audio: {e}")

    def _play_sound(self, file_name):
            path = pathlib.Path("audio") / file_name
            try:
                subprocess.run(["aplay", path], check=True)
                print(f"Reproducción de audio completada: {path}")
            except subprocess.CalledProcessError as e:
                print(f"Error al reproducir el audio {path}: {e}")
