from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QMovie
import os


class LoadingWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            QLabel#title {
                color: white;
                font-size: 40px;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)


        self.label_text = QLabel("Procesando...")
        self.label_text.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #34495e;
            font-family: 'Segoe UI', sans-serif;
        """)
        self.label_text.setAlignment(Qt.AlignCenter)

        # GIF de loading
        self.label_gif = QLabel()
        current_dir = os.path.dirname(os.path.abspath(__file__))  
        project_root = os.path.abspath(os.path.join(current_dir, "..")) 
        gif_path = os.path.join(project_root, "icons", "loading.gif") 
        movie = QMovie(gif_path)
        self.label_gif.setMovie(movie)
        movie.start()

        layout.addWidget(self.label_gif)
        layout.addWidget(self.label_text)

        self.setLayout(layout)
