from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt

class CustomLineEdit(QLineEdit):
    """
    A reusable, modern-styled QLineEdit for PySide6 applications.
    """
    def __init__(self, parent=None, placeholder_text: str = ""):
        super().__init__(parent)
        # Set basic properties
        self.setPlaceholderText(placeholder_text)
        self.setMinimumHeight(32)
        self.setClearButtonEnabled(True)
        self._apply_styles()

    def _apply_styles(self):
        """Apply modern stylesheet for normal and focus states."""
        self.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #D1D5DB;    /* light gray */
                border-radius: 8px;
                padding: 6px 10px;
                background-color: #F9FAFB;    /* very light gray */
                font-size: 14px;
                color: #111827;               /* nearly black */
            }
            QLineEdit:focus {
                border: 2px solid #3B82F6;    /* blue */
                background-color: #FFFFFF;
            }
            QLineEdit[error="true"] {
                border: 2px solid #EF4444;    /* red on error */
            }
            QLineEdit[error="true"]:focus {
                border: 2px solid #DC2626;
            }
            """
        )

    def set_error(self, has_error: bool):
        """
        Toggle an "error" state styling.
        :param has_error: True to show error border, False to reset.
        """
        self.setProperty("error", str(has_error).lower())
        self.style().unpolish(self)
        self.style().polish(self)
