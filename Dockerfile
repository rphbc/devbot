FROM python:3.8-slim-bullseye

RUN apt update && apt install ffmpeg -y


WORKDIR /app

COPY requirements.txt ./
RUN pip install -r ./requirements.txt

COPY bot.py ./

CMD ["python", "bot.py"]
