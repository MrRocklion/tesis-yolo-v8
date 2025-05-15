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
from screens.feeling_screen import FeelingScreen
from screens.gender_screen import GenderScreen
from screens.result_screen import ResultScreen
from screens.loading_screen import LoadingScreen
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
        self.settings_view = SettingScreen(stacked_widget=self.stack)
        self.menu_view = MenuScreen(stacked_widget=self.stack)
        self.gender_view = GenderScreen(stacked_widget=self.stack,controller=self.controller)
        self.age_view = AgeScreen(stacked_widget=self.stack,controller=self.controller)
        self.feeling_view = FeelingScreen(stacked_widget=self.stack,controller=self.controller)
        self.capture_view = CaptureScreen(stacked_widget=self.stack,controller=self.controller)
        self.loading_view = LoadingScreen(stacked_widget=self.stack,controller=self.controller)
        self.result_view = ResultScreen(stacked_widget=self.stack,controller=self.controller)


        self.stack.addWidget(self.settings_view)    #index 0
        self.stack.addWidget(self.menu_view) #index 1
        self.stack.addWidget(self.gender_view) #index 2
        self.stack.addWidget(self.age_view) #index 3
        self.stack.addWidget(self.feeling_view) #index 4
        self.stack.addWidget(self.capture_view) #index 5
        self.stack.addWidget(self.loading_view) #index 6
        self.stack.addWidget(self.result_view) #index 7
        self.stack.setCurrentIndex(1)
        
        main_layout.addWidget(self.stack)

        self.setStyleSheet(self.get_stylesheet())
    
    def get_stylesheet(self):
         return """
        QWidget {
            background-color: #ecf0f1;
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