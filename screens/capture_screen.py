from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QStackedWidget,QMessageBox
)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QTimer, Signal
import sys
import cv2
import requests
from requests.auth import HTTPDigestAuth
import json
from PIL import Image
import os
import time
from widgets.menu_btn import MenuButton
class CaptureScreen(QWidget):
    def __init__(self, stacked_widget,controller):
        super().__init__()
        self.controller = controller
        self.stacked_widget = stacked_widget
        self.cap = None
        self.timer = QTimer()
        self.layout = QVBoxLayout()
        self.image_label = QLabel("Iniciando cámara...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.age_label = QLabel("Edad: " + str(self.controller.get_age()))
        self.age_label.setStyleSheet("font-size: 24px; font-weight: bold;color: #212121;")
        self.age_label.setAlignment(Qt.AlignCenter)

        self.home_btn = MenuButton("Regresar al Inicio")
        self.home_btn.clicked.connect(self.regresar_a_primera_ventana)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.age_label)
        self.layout.addWidget(self.home_btn)
        self.setLayout(self.layout)
        self.controller.ageChanged.connect(self.actualizar_edad)
        self.iniciar_camara()

        

    def showEvent(self, event):
        super().showEvent(event)
        self.timer.start(30)
        

    def iniciar_camara(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.image_label.setText("No se pudo acceder a la cámara.")
            return

        self.timer.timeout.connect(self.mostrar_frame)
        self.timer.start(30) 

    def mostrar_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame_rgb.shape
            bytes_per_line = 3 * width
            q_image = QImage(
                frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.width(), self.image_label.height(),
                Qt.KeepAspectRatio
            ))
    def crop_to_portrait(self,image, aspect_ratio=(4, 5)):
        height, width, _ = image.shape
        target_ratio = aspect_ratio[0] / aspect_ratio[1]
        current_ratio = width / height

        if current_ratio > target_ratio:
            new_width = int(height * target_ratio)
            x1 = (width - new_width) // 2
            image_cropped = image[:, x1:x1 + new_width]
        else:
            new_height = int(width / target_ratio)
            y1 = (height - new_height) // 2
            image_cropped = image[y1:y1 + new_height, :]

        return image_cropped




    def recibir_datos(self, datos):
        self.userData = datos

    def regresar_a_primera_ventana(self):
        self.stacked_widget.setCurrentIndex(0)
    
    def actualizar_edad(self, nueva_edad):
        self.age_label.setText(f"Edad: {nueva_edad}")
