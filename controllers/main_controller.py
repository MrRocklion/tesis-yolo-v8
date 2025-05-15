from PySide6.QtCore import QObject, Signal

class MainController(QObject):
    ageChanged = Signal(int)
    genderChanged = Signal(str)
    emotionChanged = Signal(str)
    classObjectChanged = Signal(str)
    dataChanged = Signal(dict)

    def __init__(self):
        super().__init__()
        self._age = 0
        self._gender = "masculino"
        self._emotion = "relajado"
        self._class_yolo = ""

    def set_age(self, age: int):
        self._age = age
        self.ageChanged.emit(age)
        self.dataChanged.emit(self.get_user_data())

    def set_gender(self, gender: str):
        self._gender = gender
        self.genderChanged.emit(gender)
        self.dataChanged.emit(self.get_user_data())

    def set_emotion(self, emotion: str):
        self._emotion = emotion
        self.emotionChanged.emit(emotion)
        self.dataChanged.emit(self.get_user_data())
    
    def set_class_object(self, class_yolo: str):
        self._class_yolo = class_yolo
        self.classObjectChanged.emit(class_yolo)
        self.dataChanged.emit(self.get_user_data())

    def get_age(self) -> int:
        return self._age

    def get_gender(self) -> str:
        return self._gender

    def get_emotion(self) -> str:
        return self._emotion

    def get_user_data(self) -> dict:
        return {
            "age": self._age,
            "gender": self._gender,
            "emotion": self._emotion,
            "class_yolo": self._class_yolo  
        }

    def reset(self):
        self.set_age(0)
        self.set_gender("masculino")
        self.set_emotion("relajado")
