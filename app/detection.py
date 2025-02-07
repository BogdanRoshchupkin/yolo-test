import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO

from .utils import pil_to_bgr


def load_yolo_model(weights_path: str, device: str) -> YOLO:
    """
    Загружает модель YOLO с указанными весами и переводит её на нужное устройство.
    """
    model = YOLO(weights_path)
    model.to(device)
    return model


def draw_bboxes(image_bgr: np.ndarray, results) -> tuple[np.ndarray, list]:
    """
    Отрисовывает найденные YOLO-боксы на изображении и возвращает:
    - аннотированное изображение (BGR)
    - список с данными по боксам (bboxes)
    """
    annotated_image = image_bgr.copy()
    bboxes = []
    for result in results:
        for box in result.boxes:
            xyxy = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            bboxes.append(xyxy + [conf, cls])

            x1, y1, x2, y2 = map(int, xyxy)
            cv2.rectangle(annotated_image, (x1, y1), (x2, y2),
                          (0, 255, 0), 2)
            cv2.putText(
                annotated_image,
                text=f"{cls} {conf:.2f}",
                org=(x1, y1 - 10),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=(0, 255, 0),
                thickness=2
            )
    return annotated_image, bboxes


def detect_and_annotate_image(pil_image: Image.Image, model: YOLO,
                              classes: list[int] = [2], conf: float = 0.5
                              ) -> tuple[np.ndarray, list]:
    """
    1. Конвертирует PIL-изображение в OpenCV-формат (BGR)
    2. Выполняет детекцию
    3. Рисует bbox на копии изображения
    4. Возвращает аннотированное изображение и список bbox
    """
    image_bgr = pil_to_bgr(pil_image)
    results = model(image_bgr, classes=classes, conf=conf)
    annotated_image, bboxes = draw_bboxes(image_bgr, results)
    return annotated_image, bboxes
