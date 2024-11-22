import cv2
from detection.detector import Detector
from tracking.tracker import Tracker
from database.db_handler import DatabaseHandler
from threading import Thread

# Инициализация модулей
detector = Detector()
tracker = Tracker()
db_handler = DatabaseHandler(db_path="tracking.db")  # Укажите путь к файлу базы данных

# Список RTSP URL ваших камер
camera_urls = [
    "rtsp://test:Realmonitor@192.168.10.63:554/Streaming/Channels/101?transportmode=unicast&profile=Profile_1"
    "rtsp://test:Realmonitor@192.168.10.61:554/cam/realmonitor?channel=1&subtype=0"
]

# Функция для обработки одной камеры
def process_camera(url, camera_id):
    print(f"Подключение к камере {camera_id} по адресу {url}...")
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print(f"Ошибка: не удалось подключиться к камере {camera_id} по адресу {url}")
        return

    print(f"Камера {camera_id} успешно подключена.")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame is None:
            print(f"Ошибка: потеряно соединение с камерой {camera_id} или кадр пустой.")
            break

        # Обнаружение объектов
        detections = detector.detect(frame)
        tracks = tracker.update(detections, frame)

        # Обработка треков
        for track in tracks:
            track_id = track['track_id']
            bbox = track['bbox']
            x1, y1, x2, y2 = map(int, bbox)
            cropped_img = frame[y1:y2, x1:x2]

            # Добавление нового человека в базу данных
            if not db_handler.exists(track_id):
                image_path = f"data/camera_{camera_id}_track_{track_id}.jpg"
                cv2.imwrite(image_path, cropped_img)
                db_handler.add_person(track_id, image_path)

            # Отрисовка рамок и ID
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"ID: {track_id}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Отображение окна с результатами
        try:
            if frame is not None:
                cv2.imshow(f"Camera {camera_id}", frame)
            else:
                print(f"Предупреждение: пустой кадр от камеры {camera_id}.")
        except cv2.error as e:
            print(f"OpenCV error на камере {camera_id}: {e}")
            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print(f"Отключение камеры {camera_id} по запросу.")
            break

    cap.release()
    cv2.destroyWindow(f"Camera {camera_id}")
    print(f"Камера {camera_id} отключена.")


# Запуск потоков для каждой камеры
threads = []
for i, url in enumerate(camera_urls):
    t = Thread(target=process_camera, args=(url, i))
    t.start()
    threads.append(t)

# Ожидание завершения всех потоков
for t in threads:
    t.join()

cv2.destroyAllWindows()
print("Все камеры отключены.")
