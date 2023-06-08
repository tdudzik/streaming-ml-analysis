FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y vim netcat iputils-ping procps && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .
COPY logger.py .

COPY wait-for-kafka.sh . 
RUN chmod +x wait-for-kafka.sh

ENTRYPOINT ["./wait-for-kafka.sh", "kafka", "python", "main.py", "kafka", "9092"]
