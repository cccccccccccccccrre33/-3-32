# Используем Python 3.11
FROM python:3.11-slim

# Создаём рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . .

# Обновляем pip и ставим зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Указываем команду для запуска бота
CMD ["python", "bot.py"]
