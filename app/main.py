import io
import uvicorn
from PIL import Image

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from .config import get_device, get_weights_path, get_ip_and_port
from .utils import base64_to_pil, image_to_base64
from .detection import load_yolo_model, detect_and_annotate_image

# Инициализация приложения
app = FastAPI()

# Настройка шаблонов
templates = Jinja2Templates(directory="app/templates")

# Загрузка модели YOLO
DEVICE = get_device()
WEIGHTS_PATH = get_weights_path()
model = load_yolo_model(WEIGHTS_PATH, DEVICE)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Главная страница с HTML-формой для загрузки изображения.
    """
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/upload", response_class=HTMLResponse)
async def upload_image(request: Request, file: UploadFile = File(...)):
    """
    Обработка загруженного через HTML-форму изображения.
    Возвращает аннотированное изображение (base64) и список bbox.
    """
    contents = await file.read()
    pil_image = Image.open(io.BytesIO(contents)).convert("RGB")

    annotated_image, bboxes = detect_and_annotate_image(pil_image, model)
    result_img_base64 = image_to_base64(annotated_image)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result_img_base64,
            "bboxes": bboxes
        }
    )


@app.post("/api/detect")
async def api_detect(payload: dict):
    """
    API-метод для обработки изображения, переданного в виде base64-строки (JSON: {"image": "..."}).
    Возвращает аннотированное изображение (base64) и список bbox.
    """
    image_b64 = payload.get("image")
    if not image_b64:
        return JSONResponse(status_code=400, content={"error": "Не предоставлено изображение"})

    pil_image = base64_to_pil(image_b64)

    annotated_image, bboxes = detect_and_annotate_image(pil_image, model)
    result_img_base64 = image_to_base64(annotated_image)

    return JSONResponse(content={
        "annotated_image": result_img_base64,
        "bboxes": bboxes
    })


if __name__ == "__main__":
    ip, port = get_ip_and_port()
    uvicorn.run("app.main:app", host=ip, port=port, reload=True)
