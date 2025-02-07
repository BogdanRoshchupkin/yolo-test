import os


def get_device() -> str:
    """
    Возвращает устройство для вычислений (CPU или GPU) из переменной окружения DEVICE.
    По умолчанию возвращается 'cpu'.
    """
    return os.getenv("DEVICE", "cpu")


def get_ip_and_port() -> tuple[str, int]:
    """
    Возвращает хост и порт для запуска сервера (из переменных окружения IP и PORT).
    По умолчанию: host='0.0.0.0', port=8000
    """
    ip = os.getenv("IP", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    return ip, port


def get_weights_path() -> str:
    """
    Возвращает путь к весам YOLO (по умолчанию 'weights/yolov8m.pt').
    """
    default_weights = "weights/yolov8m.pt"
    return os.path.join(os.getcwd(), default_weights)
