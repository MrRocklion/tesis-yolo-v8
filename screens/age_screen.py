from PySide6.QtWidgets import (
    QWidget,QVBoxLayout,QLabel,QHBoxLayout
)

from PySide6.QtCore import Qt
from widgets.menu_btn import MenuButton
from widgets.number_btn import NumberButton
class AgeScreen(QWidget):
    def __init__(self, stacked_widget,controller):
        super().__init__()
        self.controller = controller
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("¿Cuántos años tienes?")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #agregamos una fila de botones
        file_buttons_1 = QHBoxLayout()
        file_buttons_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        six_btn = NumberButton("6")
        six_btn.clicked.connect(lambda: self.select_age(6))
        seven_btn = NumberButton("7")
        seven_btn.clicked.connect(lambda: self.select_age(7))
        eight_btn = NumberButton("8")
        eight_btn.clicked.connect(lambda: self.select_age(8))
        nine_btn = NumberButton("9")
        nine_btn.clicked.connect(lambda: self.select_age(9))
        file_buttons_1.addWidget(six_btn)
        file_buttons_1.addWidget(seven_btn)
        file_buttons_1.addWidget(eight_btn)
        file_buttons_1.addWidget(nine_btn)

        #agregamos una fila de botones
        file_buttons_2 = QHBoxLayout()
        file_buttons_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ten_btn = NumberButton("10")
        ten_btn.clicked.connect(lambda: self.select_age(10))
        eleven_btn = NumberButton("11")
        eleven_btn.clicked.connect(lambda: self.select_age(11))
        twelve_btn = NumberButton("12")
        twelve_btn.clicked.connect(lambda: self.select_age(12))
        thirteen_btn = NumberButton("13")
        thirteen_btn.clicked.connect(lambda: self.select_age(13))
        file_buttons_2.addWidget(ten_btn)
        file_buttons_2.addWidget(eleven_btn)
        file_buttons_2.addWidget(twelve_btn)
        file_buttons_2.addWidget(thirteen_btn)

        return_btn = MenuButton("Regresar al Inicio")
        return_btn.clicked.connect(lambda: self.change_view(0))


        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addLayout(file_buttons_1)
        layout.addSpacing(20)
        layout.addLayout(file_buttons_2)
        layout.addSpacing(20)
        layout.addWidget(return_btn)

        self.setLayout(layout)
    
    def change_view(self,index):
        self.stacked_widget.setCurrentIndex(index)
    def select_age(self,age):
        self.controller.set_age(age)
        self.stacked_widget.setCurrentIndex(3)

        




