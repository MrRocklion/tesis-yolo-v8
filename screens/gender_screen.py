from PySide6.QtWidgets import (
    QWidget,QVBoxLayout,QLabel,QHBoxLayout
)

from PySide6.QtCore import Qt
from widgets.menu_btn import MenuButton
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
            font-size: 84px;
            font-weight: bold;
            color: #34495e;
            font-family: 'Segoe UI', sans-serif;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #agregamos una fila de botones
        file_buttons_1 = QHBoxLayout()
        file_buttons_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        male_btn = GenderButton(text="Niño", name="male")
        male_btn.clicked.connect(lambda: self.select_gender("masculino"))
        female_btn = GenderButton(text="Niña", name="female")
        female_btn.clicked.connect(lambda: self.select_gender("femenino"))
       
        file_buttons_1.addWidget(male_btn)
        file_buttons_1.addWidget(female_btn)




    #    # ... código anterior ...

    #     return_btn = MenuButton("Regresar al Inicio")
    #     return_btn.setFixedSize(160, 50)  # Puedes ajustar esto como desees
    #     return_btn.clicked.connect(lambda: self.change_view(1))

    #     return_layout = QHBoxLayout()
    #     return_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    #     return_layout.addWidget(return_btn)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addLayout(file_buttons_1)
        #layout.addLayout(return_layout)  # <-- Aquí lo agregas envuelto

        self.setLayout(layout)

    
    def change_view(self,index):
        self.stacked_widget.setCurrentIndex(index)

    def select_gender(self,gender):
        self.controller.set_gender(gender)
        self.stacked_widget.setCurrentIndex(3)

        




