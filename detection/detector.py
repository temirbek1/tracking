import torch

class Detector:
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    def detect(self, frame):
        results = self.model(frame)
        detections = []
        for box in results.xyxy[0]:  # Обработка результатов YOLO
            x1, y1, x2, y2, conf, cls = box.tolist()
            if int(cls) == 0:  # Только для людей
                detections.append({'bbox': (x1, y1, x2, y2), 'confidence': conf})
        return detections
