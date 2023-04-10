FROM python:3.8-slim

WORKDIR /locotrocoBot


RUN apt update && apt install -y --no-install-recommends ffmpeg 

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ARG DISCORD_TOKEN
ARG W2G_TOKEN
ARG GENIUS_TOKEN

ENV DISCORD_TOKEN=${DISCORD_TOKEN}
ENV GENIUS_TOKEN=${GENIUS_TOKEN}
ENV W2G_TOKEN=${W2G_TOKEN}

COPY ./src .

CMD [ "python", "./main.py" ]
