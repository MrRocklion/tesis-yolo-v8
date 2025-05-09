from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QStackedWidget, QLabel, QHBoxLayout, QMainWindow
)
from PySide6.QtCore import Qt
import sys
from controllers.main_controller import MainController
from screens.menu_screen import MenuScreen
from screens.age_screen  import AgeScreen
from screens.settings_screen import SettingScreen
from screens.capture_screen import CaptureScreen
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = MainController()
        self.setWindowTitle("Reconocimiento de Patrones - Joan David Encarnacion Diaz")
        self.setMinimumSize(800, 300)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        #contenedor de vistas
        self.stack = QStackedWidget()
        self.menu_view = MenuScreen(stacked_widget=self.stack)
        self.age_view = AgeScreen(stacked_widget=self.stack,controller=self.controller)
        self.capture_view = CaptureScreen(stacked_widget=self.stack,controller=self.controller)
        self.settings_view = SettingScreen(stacked_widget=self.stack)

        self.stack.addWidget(self.menu_view)
        self.stack.addWidget(self.age_view)
        self.stack.addWidget(self.settings_view)
        self.stack.addWidget(self.capture_view)
        self.stack.setCurrentIndex(0)
        
        main_layout.addWidget(self.stack)

        self.setStyleSheet(self.get_stylesheet())
    
    def get_stylesheet(self):
         return """
        QWidget {
            background-color: #FAFAFA;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }

        #titleLabel {
            font-size: 24px;
            color: #212121;
        }


        """
        
        

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec())