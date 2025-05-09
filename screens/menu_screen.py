from PySide6.QtWidgets import (
    QWidget,QVBoxLayout,QLabel,QSizePolicy
)

from PySide6.QtCore import Qt

from widgets.start_btn import StartButton
from widgets.exit_btn import ExitButton
from widgets.settings_btn import SettingsButton
class MenuScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        layout.setContentsMargins(80, 0, 80, 0) 
        layout.setSpacing(20)
        title = QLabel("MENU PRINCIPAL")
        title.setStyleSheet("""
            font-size: 84px;
            font-weight: bold;
            color: #34495e;
            font-family: 'Segoe UI', sans-serif;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        age_btn = StartButton("INICIAR", lambda: self.change_view(2))
        exit_btn = ExitButton("SALIR")
        exit_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        settings_btn = SettingsButton("AJUSTES", lambda: self.change_view(0))

        #agregamos los widgets al layout
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(age_btn)
        layout.addSpacing(20)
        layout.addWidget(settings_btn)
        layout.addSpacing(20)
        layout.addWidget(exit_btn)
        self.setLayout(layout)
    
    def change_view(self,index):
        self.stacked_widget.setCurrentIndex(index)

        




