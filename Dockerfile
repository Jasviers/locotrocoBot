FROM python:3.8

WORKDIR /home/jasviers/repos/locotrocoBot

RUN apt-get update
RUN apt-get -y install ffmpeg

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "python", "./src/main.py" ]