# Используется официальный образ Python как базовый
FROM python:3.9-alpine

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем содержимое текущей папки в /app внутри контейнера
COPY . /app

# Обновляем индекс пакетов и ставим системные зависимости
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Устанавливаем Python-зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 5000
EXPOSE 5000

# Запускаем app.py при старте контейнера
CMD ["python", "app.py"]