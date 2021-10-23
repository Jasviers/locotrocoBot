FROM python:3.8-slim

WORKDIR /locotrocoBot

RUN apt update && apt install -y ffmpeg

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "python", "./src/main.py" ]