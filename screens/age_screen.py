from PySide6.QtWidgets import (
    QWidget,QVBoxLayout,QLabel,QPushButton
)

from PySide6.QtCore import Qt
from widgets.menu_btn import MenuButton
class AgeScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Age SCREEN")
        title.setObjectName("ageTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button = MenuButton("Regresar al Inicio")
        button.clicked.connect(self.change_view)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(button)

        self.setLayout(layout)
    
    def change_view(self):
        self.stacked_widget.setCurrentIndex(0)

        




