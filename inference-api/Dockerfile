FROM python:3.11

RUN apt-get update && apt-get install -y vim netcat iputils-ping procps && rm -rf /var/lib/apt/lists/

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80


ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"] 
