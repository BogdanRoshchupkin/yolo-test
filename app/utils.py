import io
import base64
import cv2
import numpy as np
from PIL import Image


def pil_to_bgr(pil_image: Image.Image) -> np.ndarray:
    """
    Конвертирует PIL-изображение в numpy-массив (OpenCV BGR).
    """
    image_array = np.array(pil_image)  # RGB
    image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    return image_bgr


def bgr_to_pil(image_bgr: np.ndarray) -> Image.Image:
    """
    Конвертирует OpenCV (BGR) в PIL (RGB).
    """
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(image_rgb)


def image_to_base64(image_bgr: np.ndarray) -> str:
    """
    Конвертирует изображение (OpenCV BGR) в base64-строку (PNG).
    """
    pil_img = bgr_to_pil(image_bgr)
    buffered = io.BytesIO()
    pil_img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def base64_to_pil(image_b64: str) -> Image.Image:
    """
    Декодирует base64-строку в PIL-изображение.
    """
    image_data = base64.b64decode(image_b64)
    return Image.open(io.BytesIO(image_data)).convert("RGB")
