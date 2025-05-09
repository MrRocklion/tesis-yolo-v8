from PySide6.QtWidgets import QPushButton
class MenuButton(QPushButton):
    def __init__(self,text:str):
        super().__init__()
        self.setText(text)
        self.setStyleSheet(self.styles())
        self.setMinimumHeight(50)
        self.setMinimumWidth(200)

    def styles(self):
        return """

            QPushButton {
                background-color: #6200EE;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                min-width: 120px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 800;
            }

            QPushButton:hover {
                background-color: #3700B3;
            }

            QPushButton:pressed {
                background-color: #30009C;
            }

        """
