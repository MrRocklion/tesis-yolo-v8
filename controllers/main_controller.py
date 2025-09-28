from PySide6.QtCore import QObject, Signal

class MainController(QObject):
    ageChanged = Signal(int)
    genderChanged = Signal(str)
    emotionChanged = Signal(str)
    classObjectChanged = Signal(str)
    yoloChanged = Signal(bool)
    dataChanged = Signal(dict)
    gptPredictionChanged = Signal(str)
    fileNameChanged = Signal(str)
    nameChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self._age = 0
        self._gender = "masculino"
        self._emotion = "relajado"
        self._class_yolo = ""
        self._yolo = False
        self._gpt_prediction = ""
        self._file_name = ""
        self._name = "David"

    def set_name(self, name: str):
        self._name = name
        self.nameChanged.emit(name)
        self.nameChanged.emit(self.get_name())

    def set_yolo(self, yolo: bool):
        self._yolo = yolo
        self.yoloChanged.emit(yolo)
        self.yoloChanged.emit(self.get_yolo())

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
    
    def set_gpt_prediction(self, prediction: str):
        self._gpt_prediction = prediction
        self.gptPredictionChanged.emit(prediction)
        self.gptPredictionChanged.emit(self.get_gpt_prediction())
    
    def set_file_name(self, file_name: str):
        self._file_name = file_name
        self.fileNameChanged.emit(file_name)
        self.fileNameChanged.emit(self.get_file_name())
        

    def get_age(self) -> int:
        return self._age

    def get_gender(self) -> str:
        return self._gender

    def get_emotion(self) -> str:
        return self._emotion

    def get_name(self) -> str:
        return self._name

    def get_user_data(self) -> dict:
        return {
            "age": self._age,
            "gender": self._gender,
            "emotion": self._emotion,
            "class_yolo": self._class_yolo  
        }
    def get_yolo(self) -> bool:
        return self._yolo
    
    def get_gpt_prediction(self) -> str:
        return self._gpt_prediction
    
    def get_file_name(self) -> str:
        return self._file_name

    def reset(self):
        self.set_age(0)
        self.set_gender("masculino")
        self.set_emotion("relajado")
