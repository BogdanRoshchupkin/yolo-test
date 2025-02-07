# Используем базовый образ с Python 3.10
FROM python:3.10-slim

# Устанавливаем системные зависимости 
RUN apt-get update && apt-get install -y build-essential libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Добавляем переменную окружения PYTHONPATH
ENV PYTHONPATH=/app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Экспортируем порт (по умолчанию 8000, но его можно задать через переменную окружения)
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "-m", "app.main"]