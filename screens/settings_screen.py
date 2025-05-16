from PySide6.QtWidgets import (
    QWidget,QVBoxLayout,QLabel
)

from PySide6.QtCore import Qt
from widgets.menu_btn import MenuButton
from widgets.custom_line_edit import CustomLineEdit
class SettingScreen(QWidget):
    def __init__(self, stacked_widget,controller):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.controller = controller
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Configuraciones")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        self.name = CustomLineEdit(placeholder_text="Nombre")
        self.name.setMaximumWidth(290)
        self.name.setText("David")
        button = MenuButton("Regresar")
        button.clicked.connect(self.change_view)

        #agregamos los widgets al layout
        layout.addWidget(title)
        layout.addSpacing(60)
        layout.addWidget(self.name)  
        layout.addSpacing(20)
        layout.addWidget(button)

        self.setLayout(layout)
    
    def change_view(self):
        if self.name.text() == "":
            self.name.set_error(True)
            return
        self.controller.set_name(self.name.text().upper())
        self.stacked_widget.setCurrentIndex(1)

        




