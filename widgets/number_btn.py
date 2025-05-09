from PySide6.QtWidgets import QPushButton
class NumberButton(QPushButton):
    def __init__(self,text:str):
        super().__init__()
        self.setText(text)
        self.setStyleSheet(self.styles())
        self.setMinimumHeight(50)
        self.setMinimumWidth(50)

    def styles(self):
        return """

            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 20px 20px;
                min-width: 120px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 34px;
                font-weight: 800;
            }

            QPushButton:hover {
                background-color: #5499c7;
            }

            QPushButton:pressed {
                background-color: #5499c7;
            }

        """
