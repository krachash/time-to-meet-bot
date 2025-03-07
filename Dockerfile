# Используем официальный образ Python 3.10 (если у вас другая версия, замените на нужную)
FROM python:3.13-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Команда для запуска вашего приложения (бота)
CMD ["python", "bot.py"]
