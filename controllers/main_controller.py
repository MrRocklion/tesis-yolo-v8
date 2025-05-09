from PySide6.QtCore import QObject, Signal

class MainController(QObject):
    ageChanged = Signal(int)

    def __init__(self):
        super().__init__()
        self._age = 0

    def set_age(self, age):
        self._age = age
        self.ageChanged.emit(age)

    def get_age(self):
        return self._age
