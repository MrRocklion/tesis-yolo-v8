from PySide6.QtWidgets import QToolButton
from PySide6.QtGui import QIcon, QPixmap, QColor,QPainter
from PySide6.QtCore import Qt
from PySide6.QtSvg import QSvgRenderer
import os

class GenderButton(QToolButton):
    def __init__(self, text: str, name: str):
        super().__init__()

        self.setText(text)

        current_dir = os.path.dirname(os.path.abspath(__file__))  
        project_root = os.path.abspath(os.path.join(current_dir, "..")) 
        icon_path = os.path.join(project_root, "icons", f"{name}.svg")  # SVG

        # Cargar el ícono como QPixmap y establecerlo
        pixmap = self.render_colored_icon(icon_path, QColor("#FF5733"))
        icon_path = os.path.join(project_root, "icons", "exit.svg") 
        self.setIcon(QIcon(icon_path))
        self.setIcon(QIcon(pixmap))
        self.setIconSize(pixmap.size())
        self.setIconSize(pixmap.size())  # Asegura que el ícono no se reduzca
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.setStyleSheet(self.styles())
        self.setMinimumSize(100, 120)

    def render_colored_icon(self, svg_path: str, color: QColor) -> QPixmap:
        """Renderiza un archivo SVG con un color personalizado."""
        renderer = QSvgRenderer(svg_path)
        pixmap = QPixmap(240, 240) 
        pixmap.fill(Qt.transparent) 

        painter = QPainter(pixmap)
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        renderer.render(painter)
        painter.end()

        return pixmap

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
