from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon, QPixmap, QColor,QPainter
from PySide6.QtCore import Qt
from PySide6.QtSvg import QSvgRenderer
import os

class SettingsButton(QPushButton):
    def __init__(self, text: str, callback):
        super().__init__()
        self.setText(text)
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Carpeta actual del script
        project_root = os.path.abspath(os.path.join(current_dir, ".."))  # Subir dos niveles
        icon_path = os.path.join(project_root, "icons", "gear.svg") 
        pixmap = self.render_colored_icon(icon_path, QColor("#FF5733"))
        self.setIcon(QIcon(icon_path))
        self.setIcon(QIcon(pixmap))
        self.setIconSize(pixmap.size())
        self.setStyleSheet(self.styles())
        self.setMinimumHeight(50)
        self.setMinimumWidth(30)
        self.clicked.connect(callback)
    
    def render_colored_icon(self, svg_path: str, color: QColor) -> QPixmap:
        """Renderiza un archivo SVG con un color personalizado."""
        renderer = QSvgRenderer(svg_path)
        pixmap = QPixmap(48, 48)  
        pixmap.fill(Qt.transparent) 

        painter = QPainter(pixmap)
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)  
        renderer.render(painter)
        painter.end()

        return pixmap

    def styles(self):
        return """
            QPushButton {
                background-color: #808b96;
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
                background-color: #cacfd2;
            }

            QPushButton:pressed {
                background-color: #909497;
            }
        """