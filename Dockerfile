FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir pyrogram python-dotenv pytz yt-dlp instaloader requests

COPY . .

CMD ["python", "main.py"]