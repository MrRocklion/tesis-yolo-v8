from PySide6.QtWidgets import QToolButton
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
import os

class EmotionButton(QToolButton):
    def __init__(self, text: str, name: str):
        super().__init__()

        self.setText(text)

        current_dir = os.path.dirname(os.path.abspath(__file__))  
        project_root = os.path.abspath(os.path.join(current_dir, "..")) 
        icon_path = os.path.join(project_root, "icons", f"{name}.png")  # PNG instead of SVG

        # Cargar el ícono como QPixmap y establecerlo
        pixmap = QPixmap(icon_path)
        icon = QIcon(pixmap)
        self.setIcon(icon)
        self.setIconSize(pixmap.size())  # Asegura que el ícono no se reduzca
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.setStyleSheet(self.styles())
        self.setMinimumSize(100, 120)


    def styles(self):
        return """
            QToolButton {
                background-color: transparent;
                color: #34495e;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 34px;
                font-weight: bold;
            }
            QToolButton:hover {
                background-color: #d0d3d4;
            }

            QToolButton:pressed {
                background-color: #bdc3c7;
            }
        """
