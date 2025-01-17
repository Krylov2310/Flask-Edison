import os
import cv2
import numpy as np

from models import ImageFeed, DetectedObject
from files import db

VOC_LABELS = [
    "background", "aeroplane", "bicycle", "bird", "boat", "bottle",
    "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant",
    "sheep", "sofa", "train", "tvmonitor"
]

file_path = os.path.abspath(os.path.dirname(__name__))
STORAGE2 = os.path.join(file_path, 'files/static/media_file/detect_file/')
STORAGE = os.path.join(file_path, 'files/static/media_file/')


def process_image(id):
    try:
        # Передаем на обработку загруженное изображение
        image_feeds = ImageFeed.query.get_or_404(id)
        image_path = STORAGE + image_feeds.image  # Определяем полный путь к файлу

        model_path = 'files/mobilenet_iter_73000.caffemodel'
        config_path = 'files/mobilenet_ssd_deploy.prototxt'
        net = cv2.dnn.readNetFromCaffe(config_path, model_path)

        img = cv2.imread(image_path)
        if img is None:
            print("Не удалось загрузить изображение")
            return False

        h, w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, 0.007843, (300, 300), 127.5)

        net.setInput(blob)
        detections = net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.6:
                class_id = int(detections[0, 0, i, 1])
                class_label = VOC_LABELS[class_id]
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)
                label = f"{class_label}: {confidence:.2f}"
                cv2.putText(img, label, (startX + 5, startY + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Строим путь для нового файла
                img_feed = STORAGE2 + image_feeds.image
                confidence2 = round(float(confidence), 2)

                result, encoded_img = cv2.imencode('.jpg', img)
                i = f'detect_file/{image_feeds.image}'
                try:
                    img_feeds = ImageFeed.query.get(id)
                    img_feeds.processed_image = i
                    db.session.add(img_feeds)
                    db.session.flush()

                    detect = DetectedObject(
                        image_feed=img_feeds.id,
                        object_type=class_label,
                        location=f"{startX},{startY},{endX},{endY}",
                        confidence=float(confidence2),
                    )
                    db.session.add(detect)
                    db.session.flush()
                    db.session.commit()
                except:
                    db.session.rollback()  # Откат базы при ошибке
                    return 'Не вышло'

        # Декодируем картинку
        if result:
            # Сохраняем новый файл
            output_path = img_feed
            with open(output_path, 'wb') as file:
                file.write(encoded_img)

        return True

    except:
        print("Файл не найден.")
        return False


# Разрешение на создание формы
def create_form(obj=None):
    return process_image(
        super(DetectedObject).create_form(obj))


# Разрешение на редакрирование формы
def edit_form(obj=None):
    return process_image(
        super(DetectedObject).edit_form(obj))
