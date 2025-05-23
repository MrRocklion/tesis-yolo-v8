from PySide6.QtWidgets import (
    QWidget,QVBoxLayout,QLabel,QHBoxLayout
)

from PySide6.QtCore import Qt
from widgets.gender_btn import GenderButton
class GenderScreen(QWidget):
    def __init__(self, stacked_widget,controller):
        super().__init__()
        self.controller = controller
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("¿Como te identificas?")
        title.setStyleSheet("""
            font-size: 64px;
            font-weight: bold;
            color: #34495e;
            font-family: 'Segoe UI', sans-serif;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #agregamos una fila de botones
        file_buttons_1 = QHBoxLayout()
        file_buttons_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        male_btn = GenderButton(text="Niño", name="male")
        male_btn.clicked.connect(lambda: self.select_gender("male"))
        female_btn = GenderButton(text="Niña", name="female")
        female_btn.clicked.connect(lambda: self.select_gender("female"))
       
        file_buttons_1.addWidget(male_btn)
        file_buttons_1.addSpacing(20)
        file_buttons_1.addWidget(female_btn)
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addLayout(file_buttons_1)


        self.setLayout(layout)

    
    def change_view(self,index):
        self.stacked_widget.setCurrentIndex(index)

    def select_gender(self,gender):
        self.controller.set_gender(gender)
        self.stacked_widget.setCurrentIndex(3)

        




