from PySide6.QtWidgets import (
    QWidget,QVBoxLayout,QLabel,QHBoxLayout
)
from PySide6.QtCore import Qt
from widgets.menu_btn import MenuButton
from widgets.emotion_button import EmotionButton
class FeelingScreen(QWidget):
    def __init__(self, stacked_widget,controller):
        super().__init__()
        self.controller = controller
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("¿Como te Sientes Hoy?")
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
        happy_btn = EmotionButton(text="Contento", name="happy")
        happy_btn.clicked.connect(lambda: self.select_feeling("happy"))

        angry_btn = EmotionButton(text="Enojado", name="angry")
        angry_btn.clicked.connect(lambda: self.select_feeling("angry"))

        sad_btn = EmotionButton(text="Triste", name="sad")
        sad_btn.clicked.connect(lambda: self.select_feeling("sad"))

        bored_btn = EmotionButton(text="Aburrido", name="bored")
        bored_btn.clicked.connect(lambda: self.select_feeling("bored"))

        relaxed_btn = EmotionButton(text="Relajado", name="relaxed")
        relaxed_btn.clicked.connect(lambda: self.select_feeling("relaxed"))
       
        file_buttons_1.addWidget(happy_btn)
        file_buttons_1.addWidget(angry_btn)
        file_buttons_1.addWidget(sad_btn)
        file_buttons_1.addWidget(bored_btn)
        file_buttons_1.addWidget(relaxed_btn)



       # ... código anterior ...

        return_btn = MenuButton("Regresar al Inicio")
        return_btn.setFixedSize(160, 50)  # Puedes ajustar esto como desees
        return_btn.clicked.connect(lambda: self.change_view(1))

        return_layout = QHBoxLayout()
        return_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return_layout.addWidget(return_btn)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addLayout(file_buttons_1)
        layout.addSpacing(40)
        #layout.addLayout(return_layout)  # <-- Aquí lo agregas envuelto

        self.setLayout(layout)

    
    def change_view(self,index):
        self.stacked_widget.setCurrentIndex(index)

    def select_feeling(self,emotion):
        self.controller.set_emotion(emotion)
        self.controller.set_yolo(True)
        self.stacked_widget.setCurrentIndex(5)

        




