from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QColor


class CustomButton(QPushButton):
    def __init__(self, text: str, base_color: str = "#6200EE"):
        super().__init__()
        self.setText(text)
        self.base_color = QColor(base_color)
        self.hover_color = self._adjust_brightness(self.base_color, factor=0.85)
        self.pressed_color = self._adjust_brightness(self.base_color, factor=0.70)

        self.setStyleSheet(self._generate_stylesheet())
        self.setMinimumHeight(50)
        self.setMinimumWidth(200)

    def _adjust_brightness(self, color: QColor, factor: float) -> str:
        """Oscurece un color multiplicando sus componentes RGB."""
        r = int(color.red() * factor)
        g = int(color.green() * factor)
        b = int(color.blue() * factor)
        return f"rgb({r},{g},{b})"

    def _generate_stylesheet(self) -> str:
        base = self.base_color.name()
        hover = self.hover_color
        pressed = self.pressed_color

        return f"""
            QPushButton {{
                background-color: {base};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                min-width: 120px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 800;
            }}

            QPushButton:hover {{
                background-color: {hover};
            }}

            QPushButton:pressed {{
                background-color: {pressed};
            }}
        """
