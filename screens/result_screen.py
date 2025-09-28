from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from widgets.custom_btn import CustomButton
import pathlib
import threading
import subprocess

class ResultScreen(QWidget):
    def __init__(self, stacked_widget, controller):
        super().__init__()
        self.controller = controller
        self.stacked_widget = stacked_widget
        self.audio_thread = None  # 🔹 Guardará el hilo activo de audio

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

        # BOTONES
        self.btn_retry = CustomButton("Reintentar", base_color="#6200EE")
        self.btn_back = CustomButton("Volver al menú", base_color="#58d68d")
        self.btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_retry.clicked.connect(lambda: self.retry_event())

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.btn_retry)
        horizontal_layout.setSpacing(20)
        horizontal_layout.addWidget(self.btn_back)
        layout.addWidget(self.result_label)
        layout.addSpacing(20)
        layout.addLayout(horizontal_layout)

        # Conectar señales
        self.controller.gptPredictionChanged.connect(self.see_result)
        self.controller.fileNameChanged.connect(self.reproducir_audio)

        self.setLayout(layout)

    def see_result(self, prediction):
        self.result_label.setText(prediction)

    def retry_event(self):
        self.stacked_widget.setCurrentIndex(5)
        self.controller.set_yolo(True)

    def reproducir_audio(self, file_name):
        """Reproduce el audio solo si no hay otro en ejecución."""
        ruta = pathlib.Path("audio") / file_name

        if not ruta.exists():
            print(f"❌ El archivo {ruta} no existe.")
            return

        # 🔹 Evitar lanzar múltiples reproducciones al mismo tiempo
        if self.audio_thread and self.audio_thread.is_alive():
            print("⚠️ Ya hay un audio reproduciéndose, espera a que termine.")
            return

        # Crear un nuevo hilo de reproducción
        self.audio_thread = threading.Thread(
            target=self._play_sound, args=(ruta,), daemon=True
        )
        self.audio_thread.start()

    def _play_sound(self, ruta: pathlib.Path):
        """Reproduce el audio usando mpg123 (más estable que aplay para MP3)."""
        try:
            print(f"▶️ Reproduciendo: {ruta}")
            subprocess.run(["mpg123", str(ruta)], check=True)
            print(f"✅ Reproducción completada: {ruta}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al reproducir {ruta}: {e}")
