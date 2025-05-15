from PySide6.QtWidgets import (QWidget, QVBoxLayout)
from PySide6.QtCore import Qt

class ResultScreen(QWidget):
    def __init__(self, stacked_widget,controller):
        super().__init__()
        self.controller = controller
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

