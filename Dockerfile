FROM python:3.7.16-slim-bullseye

WORKDIR app

COPY requirements.txt .
COPY bot.py .

RUN pip install -r requirements.txt
RUN apt update && apt install ffmpeg -y

CMD ["python", "bot.py"]
