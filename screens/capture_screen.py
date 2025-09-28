from PySide6.QtWidgets import ( QWidget, QVBoxLayout,
    QLabel
)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QTimer
import cv2
import os
import time
from yolov8 import YOLOv8
current_dir = os.path.dirname(os.path.abspath(__file__))  
project_root = os.path.abspath(os.path.join(current_dir, "..")) 
model_path = os.path.join(project_root, "models", f"best.onnx")
class CaptureScreen(QWidget):
    def __init__(self, stacked_widget,controller):
        super().__init__()
        #parametros yolo
        self.yolov8_detector = YOLOv8("models/best.onnx", conf_thres=0.5, iou_thres=0.5)
        self.start=False
        self.detection_duration = 3
        self.score_threshold = 0.8
        self.image_path = "target.jpg"
        self.detection_timers = {}
        self.cooldown = 5
        self.controller = controller
        self.stacked_widget = stacked_widget
        self.cap = None
        self.timer = QTimer()
        self.layout = QVBoxLayout()
        self.image_label = QLabel("Iniciando cámara...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label,4)
        self.setLayout(self.layout)
        self.controller.yoloChanged.connect(self.yoloActivate)
        self.iniciar_camara()

        

    def enable_yolo(self, event):
        super().showEvent(event)
        self.start = True
        

    def iniciar_camara(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.image_label.setText("No se pudo acceder a la cámara.")
            self.start = False
            self.stacked_widget.setCurrentIndex(1)
            return

        self.timer.timeout.connect(self.mostrar_frame)
        self.timer.start(30)

    def on_object_identified(self):
        self.start = False
        self.stacked_widget.setCurrentIndex(6)
    


    def mostrar_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame_start = time.time()
            if self.start:
                boxes, scores, class_ids = self.yolov8_detector(frame)
            else:
                boxes, scores, class_ids = [], [], []
            current_time = time.time()
            
            for box, score, class_id in zip(boxes, scores, class_ids):
                x1, y1, x2, y2 = map(int, box)
                label = f"ID: {class_id} ({score:.2f})"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, max(y1 - 10, 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Manejo del temporizador para objetos con score alto

                if score >= self.score_threshold:
                    if class_id not in self.detection_timers:
                        self.detection_timers[class_id] = current_time
                    else:
                        elapsed = current_time - self.detection_timers[class_id]
                        if elapsed >= self.detection_duration:
                            # Extraer región del objeto y guardarla
                            object_crop = frame[y1:y2, x1:x2]
                            if object_crop.size > 0:
                                cv2.imwrite('target.jpg', object_crop)
                                self.on_object_identified()
                            else:
                                print("Región de objeto vacía, no se guardó imagen.")
                            self.detection_timers[class_id] = float('inf')  # evitar múltiples disparos
                else:
                    self.detection_timers.pop(class_id, None) 
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame_rgb.shape
            bytes_per_line = 3 * width
            q_image = QImage(
                frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.width(), self.image_label.height(),
                Qt.KeepAspectRatio
            ))
            frame_end = time.time()
            fps = 1 / (frame_end - frame_start)


    def crop_to_portrait(self,image, aspect_ratio=(4, 5)):
        height, width, _ = image.shape
        target_ratio = aspect_ratio[0] / aspect_ratio[1]
        current_ratio = width / height

        if current_ratio > target_ratio:
            new_width = int(height * target_ratio)
            x1 = (width - new_width) // 2
            image_cropped = image[:, x1:x1 + new_width]
        else:
            new_height = int(width / target_ratio)
            y1 = (height - new_height) // 2
            image_cropped = image[y1:y1 + new_height, :]

        return image_cropped
        
    def yoloActivate(self,data):
        self.start = data


